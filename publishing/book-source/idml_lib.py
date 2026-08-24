# -*- coding: utf-8 -*-
"""Minimal IDML (InDesign Markup Language) writer.

Emits a valid .idml package: designmap, resources, master spread, spreads, stories.
Geometry is in points. Page-local coordinates are converted to spread space by the Page
object's offset, so callers think in ordinary page coordinates.
"""
import os, zipfile, html as _html
from pathlib import Path

DOM = "17.0"
PKG = 'xmlns:idPkg="http://ns.adobe.com/AdobeInDesign/idml/1.0/packaging"'
XMLDECL = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'

def esc(s):
    return _html.escape(str(s), quote=False).replace(" ", " ")

def _num(v):
    return ("%.4f" % v).rstrip("0").rstrip(".") if isinstance(v, float) else str(v)

def rect_path(w, h):
    pts = [(0, 0), (0, h), (w, h), (w, 0)]
    inner = "".join(
        '<PathPointType Anchor="%s %s" LeftDirection="%s %s" RightDirection="%s %s"/>'
        % (_num(x), _num(y), _num(x), _num(y), _num(x), _num(y)) for x, y in pts)
    return ('<Properties><PathGeometry><GeometryPathType PathOpen="false">'
            '<PathPointArray>%s</PathPointArray></GeometryPathType></PathGeometry>'
            '</Properties>' % inner)

def xform(x, y, sx=1.0, sy=1.0):
    return "%s 0 0 %s %s %s" % (_num(sx), _num(sy), _num(x), _num(y))


def link_uri(path):
    value = Path(path)
    portable = value.as_posix()
    if (
        value.is_absolute()
        or not portable
        or "\\" in portable
        or ":" in portable
        or "?" in portable
        or "#" in portable
        or any(part in ("", ".") for part in value.parts)
    ):
        raise ValueError("IDML image link must be a relative path into the archive")
    return "file:" + portable


class Story:
    """A text story. Paragraphs are (para_style, runs) where runs are
    (char_style_or_None, text) tuples. char_style None = default."""
    def __init__(self, sid):
        self.id = sid
        self.paras = []

    def para(self, style, runs):
        if isinstance(runs, str):
            runs = [(None, runs)]
        self.paras.append((style, runs))
        return self

    def xml(self):
        out = []
        n = len(self.paras)
        for i, (pstyle, runs) in enumerate(self.paras):
            out.append('<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/%s">' % pstyle)
            runs = [r for r in runs if r[1] != "" or len(runs) == 1]
            if not runs:
                runs = [(None, "")]
            for j, (cstyle, text) in enumerate(runs):
                cs = ("CharacterStyle/%s" % cstyle) if cstyle else "CharacterStyle/$ID/[No character style]"
                last = (j == len(runs) - 1)
                br = "<Br/>" if (last and i < n - 1) else ""
                out.append('<CharacterStyleRange AppliedCharacterStyle="%s">'
                           '<Content>%s</Content>%s</CharacterStyleRange>' % (cs, esc(text), br))
            out.append('</ParagraphStyleRange>')
        return (XMLDECL + '<idPkg:Story %s DOMVersion="%s">'
                '<Story Self="%s" AppliedTOCStyle="n" UserText="true" IsEndnoteStory="false" '
                'TrackChanges="false" StoryTitle="$ID/" AppliedNamedGrid="n">'
                '<StoryPreference OpticalMarginAlignment="false" OpticalMarginSize="12" '
                'FrameType="TextFrameType" StoryOrientation="Horizontal" '
                'StoryDirection="LeftToRightDirection"/>'
                '<InCopyExportOption IncludeGraphicProxies="true" IncludeAllResources="false"/>'
                '%s</Story></idPkg:Story>'
                % (PKG, DOM, self.id, "".join(out)))


class Page:
    def __init__(self, doc, spread, index_in_spread, number, recto, xoff, yoff, master="mS1"):
        self.doc, self.spread = doc, spread
        self.n = number
        self.recto = recto
        self.xoff, self.yoff = xoff, yoff
        self.master = master
        self.self_id = "%sp%d" % (spread.id, index_in_spread)

    # --- coordinate helper -------------------------------------------------
    def S(self, x, y):
        return self.xoff + x, self.yoff + y

    # --- items -------------------------------------------------------------
    def rect(self, x, y, w, h, fill="Swatch/None", stroke="Swatch/None", sw=0):
        sx, sy = self.S(x, y)
        self.spread.items.append(
            '<Rectangle Self="%s" ItemTransform="%s" AppliedObjectStyle="ObjectStyle/$ID/[None]" '
            'ItemLayer="ua" Visible="true" Name="$ID/" FillColor="%s" StrokeColor="%s" '
            'StrokeWeight="%s" ContentType="Unassigned">%s</Rectangle>'
            % (self.doc.uid("r"), xform(sx, sy), fill, stroke, _num(sw), rect_path(w, h)))

    FORMATS = {".jpg": "$ID/JPEG", ".jpeg": "$ID/JPEG",
               ".png": "$ID/Portable Network Graphics (PNG)",
               ".tif": "$ID/TIFF", ".tiff": "$ID/TIFF", ".psd": "$ID/Photoshop"}

    def image(self, x, y, w, h, link_path, px_w, px_h, fit="cover", dpi=300):
        """Place a linked image in a frame at page coords, cover- or contain-fitted."""
        sx, sy = self.S(x, y)
        nw, nh = px_w * 72.0 / dpi, px_h * 72.0 / dpi
        s = max(w / nw, h / nh) if fit == "cover" else min(w / nw, h / nh)
        ox, oy = (w - nw * s) / 2.0, (h - nh * s) / 2.0
        rid, iid = self.doc.uid("r"), self.doc.uid("img")
        uri = link_uri(link_path)
        fmt = self.FORMATS.get(os.path.splitext(link_path)[1].lower(), "$ID/JPEG")
        self.spread.items.append(
            '<Rectangle Self="%s" ItemTransform="%s" AppliedObjectStyle="ObjectStyle/$ID/[None]" '
            'ItemLayer="ua" Visible="true" Name="$ID/" FillColor="Swatch/None" '
            'StrokeColor="Swatch/None" StrokeWeight="0" ContentType="GraphicType">'
            '%s'
            '<FrameFittingOption AutoFit="true" FittingOnEmptyFrame="FillProportionally" '
            'FittingAlignment="CenterAnchor" LeftCrop="0" TopCrop="0" RightCrop="0" BottomCrop="0"/>'
            '<Image Self="%s" ItemTransform="%s" ImageTypeName="%s" '
            'AppliedObjectStyle="ObjectStyle/$ID/[None]" Visible="true" Name="$ID/" '
            'ActualPpi="%d %d" EffectivePpi="%d %d" ImageRenderingIntent="UseColorSettings">'
            '<Properties><Profile type="string">$ID/Embedded</Profile>'
            '<GraphicBounds Left="0" Top="0" Right="%s" Bottom="%s"/></Properties>'
            '<Link Self="%s" AssetURL="$ID/" AssetID="$ID/" LinkResourceURI="%s" '
            'LinkResourceFormat="%s" StoredState="Normal" LinkClassID="35906" '
            'LinkClientID="257" LinkResourceModified="false" LinkObjectModified="false" '
            'ShowInUI="true" CanEmbed="true" CanUnembed="false" CanPackage="true" '
            'ImportPolicy="NoAutoImport" ExportPolicy="NoAutoExport" LinkImportStamp="$ID/"/>'
            '</Image></Rectangle>'
            % (rid, xform(sx, sy), rect_path(w, h), iid,
               xform(sx + ox, sy + oy, s, s), fmt,
               dpi, dpi, int(round(dpi / s)), int(round(dpi / s)),
               _num(nw), _num(nh), self.doc.uid("lnk"), esc(uri), fmt))

    def text(self, x, y, w, h, story, cols=1, gutter=24, valign="TopAlign",
             prev="n", nxt="n", inset=0, name=None):
        sx, sy = self.S(x, y)
        tid = name or self.doc.uid("tf")
        ins = ("<Properties><InsetSpacing type=\"list\">"
               + "".join('<ListItem type="unit">%s</ListItem>' % _num(inset) for _ in range(4))
               + "</InsetSpacing></Properties>")
        self.spread.items.append(
            '<TextFrame Self="%s" ParentStory="%s" PreviousTextFrame="%s" NextTextFrame="%s" '
            'ContentType="TextType" ItemTransform="%s" '
            'AppliedObjectStyle="ObjectStyle/$ID/[Normal Text Frame]" ItemLayer="ua" '
            'Visible="true" Name="$ID/" FillColor="Swatch/None" StrokeColor="Swatch/None" '
            'StrokeWeight="0">%s'
            '<TextFramePreference TextColumnCount="%d" TextColumnGutter="%s" '
            'VerticalJustification="%s" FirstBaselineOffset="AscentOffset" '
            'AutoSizingType="Off" UseNoLineBreaksForAutoSizing="false">%s</TextFramePreference>'
            '<TextWrapPreference Inverse="false" ApplyToMasterPageOnly="false" '
            'TextWrapSide="BothSides" TextWrapMode="None">'
            '<Properties><TextWrapOffset Top="0" Left="0" Bottom="0" Right="0"/></Properties>'
            '</TextWrapPreference>'
            '</TextFrame>'
            % (tid, story, prev, nxt, xform(sx, sy), rect_path(w, h),
               cols, _num(gutter), valign, ins))
        self.doc.placements.append({"frame": tid, "story": story, "w": w, "h": h,
                                    "cols": cols, "gutter": gutter,
                                    "threaded": prev != "n" or nxt != "n"})
        return tid


class Spread:
    def __init__(self, doc, sid):
        self.doc, self.id, self.pages, self.items = doc, sid, [], []

    def xml(self):
        pgs = []
        for p in self.pages:
            mp = ('ColumnCount="1" ColumnGutter="12" Top="%s" Bottom="%s" Left="%s" Right="%s"'
                  % (_num(self.doc.MT), _num(self.doc.MB),
                     _num(self.doc.MI if p.recto else self.doc.MO),
                     _num(self.doc.MO if p.recto else self.doc.MI)))
            pgs.append(
                '<Page Self="%s" Name="%d" AppliedMaster="%s" OverrideList="" '
                'GeometricBounds="0 0 %s %s" ItemTransform="%s" MasterPageTransform="1 0 0 1 0 0" '
                'AppliedTrapPreset="TrapPreset/$ID/kDefaultTrapStyleName" '
                'TabOrder="" GridStartingPoint="TopOutside" UseMasterGrid="true">'
                '<MarginPreference %s ColumnDirection="Horizontal" ColumnsPositions="0 %s"/>'
                '<GridDataInformation FontStyle="Regular" PointSize="12" CharacterAki="0" '
                'LineAki="9" HorizontalScale="100" VerticalScale="100" LineAlignment="LeftOrTopLineJustify" '
                'GridAlignment="AlignEmCenter" CharacterAlignment="AlignEmCenter">'
                '<Properties><AppliedFont type="string">EB Garamond</AppliedFont></Properties>'
                '</GridDataInformation></Page>'
                % (p.self_id, p.n, p.master, _num(self.doc.H), _num(self.doc.W),
                   xform(p.xoff, p.yoff), mp,
                   _num(self.doc.W - self.doc.MI - self.doc.MO)))
        return (XMLDECL + '<idPkg:Spread %s DOMVersion="%s">'
                '<Spread Self="%s" PageTransitionType="None" PageTransitionDirection="NotApplicable" '
                'PageTransitionDuration="Medium" ShowMasterItems="true" PageCount="%d" '
                'BindingLocation="%d" AllowPageShuffle="true" ItemTransform="1 0 0 1 0 %s" '
                'FlattenerOverride="Default">'
                '<FlattenerPreference LineArtAndTextResolution="300" GradientAndMeshResolution="150" '
                'ClipComplexRegions="false" ConvertAllStrokesToOutlines="false" '
                'ConvertAllTextToOutlines="false"><Properties>'
                '<RasterVectorBalance type="double">50</RasterVectorBalance></Properties>'
                '</FlattenerPreference>%s%s</Spread></idPkg:Spread>'
                % (PKG, DOM, self.id, len(self.pages),
                   0 if (len(self.pages) == 1 and self.pages[0].recto) else 1,
                   _num(self.doc.spreads.index(self) * (self.doc.H + 180.0)),
                   "".join(pgs), "".join(self.items)))


class Doc:
    def __init__(self, W, H, bleed, MT, MB, MI, MO, facing=True):
        # bleed may be a scalar or (top, bottom, inside, outside)
        if isinstance(bleed, (tuple, list)):
            self.bleed_t, self.bleed_b, self.bleed_i, self.bleed_o = bleed
        else:
            self.bleed_t = self.bleed_b = self.bleed_i = self.bleed_o = bleed
        self.bleed = max(self.bleed_t, self.bleed_b, self.bleed_i, self.bleed_o)
        self.W, self.H = W, H
        self.facing = facing
        self.MT, self.MB, self.MI, self.MO = MT, MB, MI, MO
        self.spreads, self.stories = [], []
        self.placements = []
        self.colors, self.pstyles, self.cstyles, self.fonts = [], [], [], []
        self._n = 0
        self._page_no = 0

    def uid(self, pfx):
        self._n += 1
        return "%s%d" % (pfx, self._n)

    def story(self, sid=None):
        s = Story(sid or self.uid("u"))
        self.stories.append(s)
        return s

    # ---- page flow ----
    def add_page(self, master="mS1"):
        """Append the next page, opening a new spread when needed. Page 1 is recto."""
        self._page_no += 1
        n = self._page_no
        recto = (n % 2 == 1)
        if not self.facing:
            sp = Spread(self, self.uid("s")); self.spreads.append(sp)
            p = Page(self, sp, 0, n, True, 0, -self.H / 2.0, master)
            sp.pages.append(p); return p
        if n == 1:
            sp = Spread(self, self.uid("s")); self.spreads.append(sp)
            p = Page(self, sp, 0, n, True, 0, -self.H / 2.0, master)
            sp.pages.append(p); return p
        if recto:
            sp = self.spreads[-1]
            if len(sp.pages) >= 2 or (len(sp.pages) == 1 and sp.pages[0].recto and n != 2):
                sp = Spread(self, self.uid("s")); self.spreads.append(sp)
        else:
            sp = Spread(self, self.uid("s")); self.spreads.append(sp)
        idx = len(sp.pages)
        xoff = -self.W if not recto else 0.0
        p = Page(self, sp, idx, n, recto, xoff, -self.H / 2.0, master)
        sp.pages.append(p)
        return p

    @property
    def page_count(self):
        return self._page_no

    # ---- resources ----
    def color(self, name, c, m, y, k):
        self.colors.append((name, c, m, y, k))

    def font(self, family, styles):
        self.fonts.append((family, styles))

    def pstyle(self, name, **kw):
        self.pstyles.append((name, kw))

    def cstyle(self, name, **kw):
        self.cstyles.append((name, kw))

    # ---- xml resources ----
    def _graphic_xml(self):
        cs = ['<Color Self="Color/%s" Model="Process" Space="CMYK" ColorValue="%s %s %s %s" '
              'ColorOverride="Normal" AlternateSpace="NoAlternateColor" AlternateColorValue="" '
              'Name="%s" ColorEditable="true" ColorRemovable="true" Visible="true" '
              'SwatchCreatorID="7937"/>' % (n, _num(c), _num(m), _num(y), _num(k), n)
              for n, c, m, y, k in self.colors]
        return (XMLDECL + '<idPkg:Graphic %s DOMVersion="%s">'
                '<Swatch Self="Swatch/None" Name="None" ColorEditable="false" '
                'ColorRemovable="false" Visible="true" SwatchCreatorID="7937"/>'
                '<Color Self="Color/Black" Model="Process" Space="CMYK" ColorValue="0 0 0 100" '
                'ColorOverride="Normal" AlternateSpace="NoAlternateColor" AlternateColorValue="" '
                'Name="Black" ColorEditable="false" ColorRemovable="false" Visible="true" '
                'SwatchCreatorID="7937"/>'
                '<Color Self="Color/Paper" Model="Process" Space="CMYK" ColorValue="0 0 0 0" '
                'ColorOverride="Specialpaper" AlternateSpace="NoAlternateColor" '
                'AlternateColorValue="" Name="Paper" ColorEditable="false" ColorRemovable="false" '
                'Visible="true" SwatchCreatorID="7937"/>'
                '%s'
                '<StrokeStyle Self="StrokeStyle/$ID/Solid" Name="$ID/Solid"/>'
                '</idPkg:Graphic>' % (PKG, DOM, "".join(cs)))

    def _fonts_xml(self):
        out = []
        for i, (fam, styles) in enumerate(self.fonts):
            fs = "".join(
                '<Font Self="font%d%d" FontFamily="%s" Name="%s&#9;%s" PostScriptName="%s" '
                'Status="Installed" FontStyleName="%s" FontType="OpenTypeCFF" WritingScript="0" '
                'FullName="%s %s" FullNameNative="%s %s" FontStyleNameNative="%s" '
                'PlatformName="$ID/" Version="1.000"/>'
                % (i, j, esc(fam), esc(fam), esc(st), esc(ps), esc(st),
                   esc(fam), esc(st), esc(fam), esc(st), esc(st))
                for j, (st, ps) in enumerate(styles))
            out.append('<FontFamily Self="fam%d" Name="%s">%s</FontFamily>' % (i, esc(fam), fs))
        return (XMLDECL + '<idPkg:Fonts %s DOMVersion="%s">%s</idPkg:Fonts>'
                % (PKG, DOM, "".join(out)))

    @staticmethod
    def _style_xml(kind, name, kw):
        props, attrs = [], []
        font = kw.pop("font", None)
        leading = kw.pop("leading", None)
        tabs = kw.pop("tabs", None)
        # object-typed properties must be Properties children, never attributes,
        # or InDesign silently ignores them
        objprops = {k: kw.pop(k) for k in list(kw) if k in ("DropCapStyle", "NextStyle")}
        if font: props.append('<AppliedFont type="string">%s</AppliedFont>' % esc(font))
        if leading is not None:
            props.append('<Leading type="unit">%s</Leading>' % _num(leading))
        if tabs:
            items = "".join(
                '<ListItem type="record"><Alignment type="enumeration">%s</Alignment>'
                '<AlignmentCharacter type="string">.</AlignmentCharacter>'
                '<Leader type="string">%s</Leader>'
                '<Position type="unit">%s</Position></ListItem>' % (al, esc(ld), _num(pos))
                for pos, al, ld in tabs)
            props.append('<TabList type="list">%s</TabList>' % items)
        props.append('<BasedOn type="object">$ID/[No %s style]</BasedOn>'
                     % ("paragraph" if kind == "ParagraphStyle" else "character"))
        for k, v in objprops.items():
            props.append('<%s type="object">%s</%s>' % (k, esc(v), k))
        for k, v in kw.items():
            attrs.append('%s="%s"' % (k, _num(v) if isinstance(v, (int, float)) else esc(v)))
        return ('<%s Self="%s/%s" Name="%s" Imported="false" %s>'
                '<Properties>%s</Properties></%s>'
                % (kind, kind, name, name, " ".join(attrs), "".join(props), kind))

    def _styles_xml(self):
        ps = "".join(self._style_xml("ParagraphStyle", n, dict(kw)) for n, kw in self.pstyles)
        cs = "".join(self._style_xml("CharacterStyle", n, dict(kw)) for n, kw in self.cstyles)
        return (XMLDECL + '<idPkg:Styles %s DOMVersion="%s">'
                '<RootCharacterStyleGroup Self="uc">'
                '<CharacterStyle Self="CharacterStyle/$ID/[No character style]" '
                'Name="$ID/[No character style]" Imported="false"/>%s</RootCharacterStyleGroup>'
                '<RootParagraphStyleGroup Self="up">'
                '<ParagraphStyle Self="ParagraphStyle/$ID/[No paragraph style]" '
                'Name="$ID/[No paragraph style]" Imported="false">'
                '<Properties><AppliedFont type="string">EB Garamond</AppliedFont></Properties>'
                '</ParagraphStyle>%s</RootParagraphStyleGroup>'
                '<RootObjectStyleGroup Self="uo">'
                '<ObjectStyle Self="ObjectStyle/$ID/[None]" Name="$ID/[None]"/>'
                '<ObjectStyle Self="ObjectStyle/$ID/[Normal Graphics Frame]" '
                'Name="$ID/[Normal Graphics Frame]"/>'
                '<ObjectStyle Self="ObjectStyle/$ID/[Normal Text Frame]" '
                'Name="$ID/[Normal Text Frame]"/></RootObjectStyleGroup>'
                '<RootTableStyleGroup Self="ut">'
                '<TableStyle Self="TableStyle/$ID/[No table style]" Name="$ID/[No table style]"/>'
                '</RootTableStyleGroup>'
                '<RootCellStyleGroup Self="ucs">'
                '<CellStyle Self="CellStyle/$ID/[None]" Name="$ID/[None]"/></RootCellStyleGroup>'
                '<TOCStyle Self="TOCStyle/$ID/[No TOC style]" Name="$ID/[No TOC style]"/>'
                '</idPkg:Styles>' % (PKG, DOM, cs, ps))

    def _prefs_xml(self):
        return (XMLDECL + '<idPkg:Preferences %s DOMVersion="%s">'
                '<DocumentPreference Self="dDocPref" PageHeight="%s" PageWidth="%s" '
                'PagesPerDocument="1" FacingPages="%s" DocumentBleedTopOffset="%s" '
                'DocumentBleedBottomOffset="%s" DocumentBleedInsideOrLeftOffset="%s" '
                'DocumentBleedOutsideOrRightOffset="%s" DocumentBleedUniformSize="false" '
                'PageBinding="LeftToRight" ColumnGuideColor="Violet" MarginGuideColor="Magenta" '
                'PreserveLayoutWhenShuffling="true" AllowPageShuffle="true" '
                'OverprintBlack="true" SnippetImportUsesOriginalLocation="false" '
                'IntentDocumentPreference="PrintIntent" SlugTopOffset="0" SlugBottomOffset="0" '
                'SlugInsideOrLeftOffset="0" SlugRightOrOutsideOffset="0">'
                '<Properties><PageSize type="string">Custom</PageSize></Properties>'
                '</DocumentPreference>'
                '<TransparencyPreference Self="dTransPref" BlendingSpace="CMYK" '
                'PageIsTransparent="false"/>'
                '<ViewPreference Self="dViewPref" HorizontalMeasurementUnits="Points" '
                'VerticalMeasurementUnits="Points" RulerOrigin="SpreadOrigin" '
                'PointsPerInch="72" ShowRulers="true"/>'
                '<TextDefault Self="dTextDefault" AppliedParagraphStyle="ParagraphStyle/$ID/[No paragraph style]"/>'
                '</idPkg:Preferences>'
                % (PKG, DOM, _num(self.H), _num(self.W),
                   "true" if self.facing else "false",
                   _num(self.bleed_t), _num(self.bleed_b),
                   _num(self.bleed_i), _num(self.bleed_o)))

    def _master_xml(self):
        return (XMLDECL + '<idPkg:MasterSpread %s DOMVersion="%s">'
                '<MasterSpread Self="mS1" Name="A-Master" NamePrefix="A" BaseName="Master" '
                'ShowMasterItems="true" PageCount="2" OverriddenPageItemProps="" '
                'ItemTransform="1 0 0 1 0 0">'
                '<Page Self="mS1p1" Name="A" AppliedMaster="n" OverrideList="" '
                'GeometricBounds="0 0 %s %s" ItemTransform="1 0 0 1 %s %s" '
                'TabOrder="" GridStartingPoint="TopOutside" UseMasterGrid="true">'
                '<MarginPreference ColumnCount="1" ColumnGutter="12" Top="%s" Bottom="%s" '
                'Left="%s" Right="%s" ColumnDirection="Horizontal" ColumnsPositions="0 %s"/></Page>'
                '<Page Self="mS1p2" Name="A" AppliedMaster="n" OverrideList="" '
                'GeometricBounds="0 0 %s %s" ItemTransform="1 0 0 1 0 %s" '
                'TabOrder="" GridStartingPoint="TopOutside" UseMasterGrid="true">'
                '<MarginPreference ColumnCount="1" ColumnGutter="12" Top="%s" Bottom="%s" '
                'Left="%s" Right="%s" ColumnDirection="Horizontal" ColumnsPositions="0 %s"/></Page>'
                '</MasterSpread></idPkg:MasterSpread>'
                % (PKG, DOM,
                   _num(self.H), _num(self.W), _num(-self.W), _num(-self.H / 2.0),
                   _num(self.MT), _num(self.MB), _num(self.MO), _num(self.MI),
                   _num(self.W - self.MI - self.MO),
                   _num(self.H), _num(self.W), _num(-self.H / 2.0),
                   _num(self.MT), _num(self.MB), _num(self.MI), _num(self.MO),
                   _num(self.W - self.MI - self.MO)))

    def write(self, path):
        parts = {}
        parts["META-INF/container.xml"] = (
            XMLDECL + '<container version="1.0" '
            'xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles>'
            '<rootfile full-path="designmap.xml" media-type="text/xml"/></rootfiles></container>')
        parts["META-INF/metadata.xml"] = (
            XMLDECL + '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF '
            'xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description '
            'rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<dc:format>application/x-indesign</dc:format></rdf:Description></rdf:RDF></x:xmpmeta>')
        parts["Resources/Graphic.xml"] = self._graphic_xml()
        parts["Resources/Fonts.xml"] = self._fonts_xml()
        parts["Resources/Styles.xml"] = self._styles_xml()
        parts["Resources/Preferences.xml"] = self._prefs_xml()
        parts["MasterSpreads/MasterSpread_mS1.xml"] = self._master_xml()
        parts["XML/Tags.xml"] = (XMLDECL + '<idPkg:Tags %s DOMVersion="%s">'
                                 '<XMLTag Self="XMLTag/Root" Name="Root">'
                                 '<Properties><TagColor type="enumeration">LightBlue</TagColor>'
                                 '</Properties></XMLTag></idPkg:Tags>' % (PKG, DOM))
        parts["XML/BackingStory.xml"] = (
            XMLDECL + '<idPkg:BackingStory %s DOMVersion="%s">'
            '<XmlStory Self="backingStory" AppliedTOCStyle="n" TrackChanges="false" '
            'StoryTitle="$ID/" AppliedNamedGrid="n">'
            '<StoryPreference OpticalMarginAlignment="false" OpticalMarginSize="12" '
            'FrameType="TextFrameType" StoryOrientation="Horizontal" '
            'StoryDirection="LeftToRightDirection"/>'
            '<InCopyExportOption IncludeGraphicProxies="true" IncludeAllResources="false"/>'
            '<ParagraphStyleRange AppliedParagraphStyle="ParagraphStyle/$ID/[No paragraph style]">'
            '<CharacterStyleRange AppliedCharacterStyle="CharacterStyle/$ID/[No character style]">'
            '<XMLElement Self="di2" MarkupTag="XMLTag/Root"/>'
            '</CharacterStyleRange></ParagraphStyleRange></XmlStory></idPkg:BackingStory>'
            % (PKG, DOM))

        spread_refs, story_refs = [], []
        for sp in self.spreads:
            p = "Spreads/Spread_%s.xml" % sp.id
            parts[p] = sp.xml(); spread_refs.append(p)
        for st in self.stories:
            p = "Stories/Story_%s.xml" % st.id
            parts[p] = st.xml(); story_refs.append(p)

        dm = (XMLDECL +
              '<?aid style="50" type="document" readerVersion="6.0" featureSet="257" '
              'product="17.0(50)" ?>\n'
              '<Document %s DOMVersion="%s" Self="d" StoryList="%s" Name="REVELATION.indd" '
              'ZeroPoint="0 0" ActiveLayer="ua" CMYKProfile="$ID/" '
              'RGBProfile="$ID/" AccurateLABSpots="false">'
              '<Language Self="Language/$ID/[No Language]" Name="$ID/[No Language]" '
              'SingleQuotes="&apos;&apos;" DoubleQuotes="&quot;&quot;" '
              'PrimaryLanguageName="$ID/[No Language]" SublanguageName="$ID/[No Language]" '
              'Id="0" HyphenationVendor="$ID/" SpellingVendor="$ID/"/>'
              '<Language Self="Language/$ID/English%%3a USA" Name="$ID/English: USA" '
              'SingleQuotes="‘’" DoubleQuotes="“”" PrimaryLanguageName="$ID/English" '
              'SublanguageName="$ID/USA" Id="269" HyphenationVendor="Proximity" '
              'SpellingVendor="Proximity"/>'
              '<Layer Self="ua" Name="Layer 1" Visible="true" Locked="false" '
              'IgnoreWrap="false" ShowGuides="true" LockGuides="false" UI="true" '
              'Expendable="true" Printable="true"/>'
              '<idPkg:Graphic src="Resources/Graphic.xml"/>'
              '<idPkg:Fonts src="Resources/Fonts.xml"/>'
              '<idPkg:Styles src="Resources/Styles.xml"/>'
              '<idPkg:Preferences src="Resources/Preferences.xml"/>'
              '<idPkg:Tags src="XML/Tags.xml"/>'
              '<idPkg:MasterSpread src="MasterSpreads/MasterSpread_mS1.xml"/>'
              '%s%s'
              '<idPkg:BackingStory src="XML/BackingStory.xml"/>'
              '<NumberingList Self="NumberingList/$ID/[Default]" Name="$ID/[Default]" '
              'ContinueNumbersAcrossStories="false" ContinueNumbersAcrossDocuments="false"/>'
              '<Section Self="sec1" Length="%d" Name="" ContinueNumbering="true" '
              'IncludeSectionPrefix="false" Marker="" PageStart="%s" SectionPrefix="">'
              '<Properties><PageNumberStyle type="enumeration">Arabic</PageNumberStyle>'
              '</Properties></Section>'
              '<DocumentUser Self="dDocumentUser0" UserName="$ID/Unknown User Name" '
              'UserColor="Color/$ID/[Light Blue]"/>'
              '</Document>'
              % (PKG, DOM, " ".join(s.id for s in self.stories),
                 "".join('<idPkg:Spread src="%s"/>' % s for s in spread_refs),
                 "".join('<idPkg:Story src="%s"/>' % s for s in story_refs),
                 self.page_count, self.spreads[0].pages[0].self_id))
        parts["designmap.xml"] = dm

        if os.path.exists(path):
            os.remove(path)
        zf = zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED)
        zi = zipfile.ZipInfo("mimetype")
        zi.compress_type = zipfile.ZIP_STORED
        zf.writestr(zi, "application/vnd.adobe.indesign-idml-package")
        for name in ["designmap.xml"] + sorted(k for k in parts if k != "designmap.xml"):
            zf.writestr(name, parts[name])
        zf.close()
        return parts
