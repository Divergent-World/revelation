# -*- coding: utf-8 -*-
"""All authored prose for the book. Written in Ali Rahman's first person."""

AUTHOR = "Ali Rahman"
FOREWORD_AUTHOR = AUTHOR

FOREWORD = [
    ("drop", """I did not set out to rebuild a fourteenth-century tapestry. I set out to
read the Book of Revelation properly, and found that I could not — because the version of
it I most wanted to look at has holes in it."""),
    ("p", """The Apocalypse Tapestry at Angers is the most ambitious attempt anyone has ever
made to render Revelation as a continuous visual narrative. Six tapestries, ninety
compartments, a hundred and forty metres of wool and linen woven between 1377 and 1382.
You were meant to walk alongside it. It was, six hundred years before the medium existed,
a film."""),
    ("p", """What survives is a ruin. Roughly seventy of the ninety compartments are still
there, many damaged. The rest were cut up during the Revolution and used as horse blankets,
as insulation for the pipes of an orangery, as rags. The sequence — the thing that made it
a narrative rather than a set of pictures — has not been experiencable since the eighteenth
century."""),
    ("p", """So this book is the sequence. Ninety plates, in the original order, against the
original Revelation anchors. Where the fourteenth-century compartment survives, I made the
plate in dialogue with it. Where it is a fragment, I worked outward from what remains.
Where it is gone, I built the scene from its neighbours, from the text, and from the logic
of the cycle — and I have said so, on the page, every time."""),
    ("p", """That last part is the only thing in this book I would defend without
qualification. Every plate carries a mark: SURVIVES, FRAGMENT, or RECONSTRUCTED. Roughly a
fifth of what you are about to look at has no medieval counterpart at all. Those plates are
mine. They are arguments about what stood there, and you are free to disagree with every
one of them. A reconstruction that hides its seams is not a reconstruction; it is a
forgery."""),
    ("p", """I made the images with generative models, over six months, and I want to be
plain about that rather than coy. The method is described in full a few pages from here —
the style contract, the six colour grades, the coordinate system, the character canon, the
rules for counting sevens. It took longer to build the system than to make any individual
picture, which is the honest shape of this kind of work. The system is the authorship. Not
one image in this book was accepted because it was pretty; each was accepted because it
obeyed the same physics as the eighty-nine around it."""),
    ("p", """Some people will find that disqualifying. I would only point out that the
original was itself a translation of a translation. Hennequin de Bruges worked from an
illuminated manuscript he did not write. Nicolas Bataille's weavers worked from cartoons
they did not draw, in a material that could not hold half the detail. Nobody in that chain
was making an original, and the result is one of the great works of European art. The
Apocalypse has always been copied forward. That is how it survived at all."""),
    ("p", """What has not been touched is the text. The Revelation to John is the strangest
book in the canon and the most visually generous — it reads as though it were written to be
painted, which is presumably why so many people have tried. It is set here in the World
English Bible, unaltered, with the words of Christ in red. The plates are an argument. The
text is not, and I have kept them clearly separate on the page so you can take one without
the other."""),
    ("p", """Read it in order if you can. The cycle is built to be walked."""),
    ("sig", "Ali Rahman · Divergent World · 2026"),
]

LOSSES = [
    ("h", "Note on the Angers Cycle"),
    ("drop", """The commission was extravagant even by the standards of a fourteenth-century
French duke. Louis I of Anjou ordered the Apocalypse in or around 1377 from Nicolas
Bataille, a Parisian merchant-weaver running the largest tapestry operation in Europe. The
cartoons were painted by Hennequin de Bruges, court painter to Charles V, working from an
illuminated Apocalypse manuscript borrowed from the royal library."""),
    ("p", """The finished work ran to six tapestries. Each opened with a tall panel showing a
seated reader — John, or a figure standing in for him — beneath an architectural canopy,
and then unfolded into fourteen narrative compartments in two registers, seven above and
seven below, against alternating grounds of red and blue. Ninety compartments in all, about
a hundred and forty metres end to end and six metres tall. Nothing larger was made anywhere
in medieval Europe."""),
    ("p", """It was used as intended for perhaps a century: hung on feast days, carried
between residences, displayed at the marriage of Louis II in 1400. René of Anjou willed it
to Angers Cathedral in 1480. And there its status quietly collapsed."""),
    ("h2", "The dispersal"),
    ("p", """Tapestry is fragile in a way painting is not. It fades, it stretches, it is
eaten. By the seventeenth century the cathedral was hanging the Apocalypse only
occasionally. By the eighteenth it had stopped. In 1767 the canons discussed destroying it
outright. In 1782 they offered it for sale and received no offers at all."""),
    ("p", """During the Revolution the cathedral's property was seized and the tapestry
entered the most destructive phase of its history. It was cut into pieces. Lengths were
used as horse blankets and as bedding, to lag the pipes of an orangery, to protect a stable
floor, and simply as rags. The decorative borders, being worth least, went first."""),
    ("p", """Recovery began in 1843, when Canon Joubert of Angers started buying fragments
back, often from people with no idea what they had. Reassembly took decades and is in a
real sense unfinished. Of ninety compartments roughly seventy survive in some condition.
Several exist only as fragments — a corner, a figure, a band of border. Around twenty are
simply gone."""),
    ("h2", "What I have done with that"),
    ("p", """Every plate in this book carries one of three marks. SURVIVES means a medieval
compartment exists at Angers and this plate was made in dialogue with it. FRAGMENT means
part of the original survives and the rest is reconstructed. RECONSTRUCTED means there is
no original: the scene is known from its position in the sequence, from its Revelation
anchor, and from the compartments on either side of it, and the plate is my argument about
what stood there."""),
    ("p", """The marks are not decoration. They are the honest part of the book. Anyone who
wants to know how much of this is evidence and how much is invention can find out on every
page — which is more than most reconstructions offer, and more than the versions of this
cycle you will find reproduced elsewhere."""),
    ("p", """I should say plainly that the survival status recorded here follows the standard
published accounts of the cycle and my own reading of the surviving panels. Where I have
been uncertain I have marked the more cautious of the two options. Anyone with access to the
Musée de la Tapisserie's own conservation records will be able to correct me, and I would
welcome it."""),
]

METHOD = [
    ("h", "Note on Method"),
    ("drop", """Ninety images made over six months by four different generative models should
not look like one work. The only reason these do is that I built the system before I made
the pictures."""),
    ("h2", "The style contract"),
    ("p", """Every plate was generated against a fixed set of constraints that never changed
across the run: classical Renaissance oil painting rendered in a clean illustrative style;
painterly but controlled brushwork without chaotic texture; clear directional light with
simplified shadow shapes; realistic but stylised anatomy; strong, clean silhouettes; large
readable colour regions; simplified graphic backgrounds; no photographic realism; no visible
canvas weave."""),
    ("p", """The last two matter most. The obvious move with a tapestry source is to chase
the texture of wool, and every attempt I made to do it destabilised the image — the model
would drift into carpet, into noise, into something that read as a photograph of a textile
rather than a picture. I abandoned texture as a goal early and the work improved
immediately. This book does not imitate weaving. It reconstructs what the weaving
depicted."""),
    ("h2", "Six grades of light"),
    ("p", """The thing that holds ninety images together is not subject matter. It is light.
I wrote one colour and lighting grade for each movement — a fixed palette, a lighting
behaviour, and an atmospheric density — and every prompt in that movement loaded it
unchanged."""),
    ("p", """Movement I is ivory, soft gold, deep blue and muted crimson under centralised
radiant illumination, with clean air and no haze: divine order. Movement II breaks that
light into patches, adds ash and drifting smoke, and desaturates toward grey and burnt red.
Movement III is chiaroscuro — black, deep crimson and steel, sharp highlights against deep
shadow, no softness anywhere. Movement IV overexposes: burning gold, sulphur, molten glow,
brightness past the point of comfort. Movement V is firelight and collapse resolving into
sudden clarity, royal purple and black giving way to white. Movement VI is ambient and
source-less — pure white, emerald, crystal blue — light with no direction and no shadow,
because in the New Jerusalem there is no lamp and no sun."""),
    ("p", """Read as a sequence, the light goes: centred, broken, contrasted, overwhelming,
collapsing, eternal. The colour goes from gold and blue to white and green. That progression
is the argument of the book made in a language other than words, and it is the single
decision I am most pleased with."""),
    ("h2", "Viewer space"),
    ("p", """Direction is specified, not left to the model. Left means the viewer's left and
right means the viewer's right, in every prompt, without exception; mirrored compositions
and symmetrical flips are forbidden outright. It is the least visible part of the method and
it does the most work. Sequences read as sequences because the camera, so to speak, obeys
rules — an angel that enters from the right in one compartment does not enter from the left
in the next."""),
    ("h2", "Canon and counting"),
    ("p", """Christ appears as the Ancient of Days: white hair, full beard, cruciform halo,
robes of ivory or muted red or soft blue. John is elderly and bearded throughout, in earth
tones. Angels are never ambiguous. These are fixed across all ninety plates."""),
    ("p", """Counting is enforced separately, because Revelation is a book of exact numbers
and generative models are careless with them. Where the text says seven, there are seven —
never six, never eight — arranged asymmetrically, four against three, evenly spaced, not
overlapping, with the central figure as the axis so they can actually be counted by eye. If
you count the lamps, the seals, the trumpets or the vials in this book, they will come out
right."""),
    ("h2", "Borders"),
    ("p", """The original alternates red and blue grounds across the narrative registers, with
the reader panels in blue. Early attempts to have the model generate borders produced drift:
the iconography mutated from compartment to compartment. So borders were removed from
generation entirely and applied afterwards as fixed assets — one frame for reader panels,
one for narrative panels. Prompts specify no frame and no mat, and keep subjects clear of
the edges."""),
    ("h2", "Selection"),
    ("p", """About a hundred and sixty candidates were generated for ninety slots. I made the
choices on a single working canvas per tapestry, with candidates laid out in the two
registers of the original, so that every decision was made in the context of its neighbours
rather than in isolation. A plate that was excellent on its own and wrong beside the two
next to it did not survive. The images in this book are what came through that."""),
    ("h2", "The models"),
    ("p", """The run began in March 2026 and moved through four models as capability improved.
The style contract did not change. Where an early plate could not hold the quality of the
later work I regenerated it rather than upscaling it, on the principle that an invented
detail is worse than an honest absence."""),
    ("h2", "The text"),
    ("p", """Scripture is the World English Bible, a public-domain modern-English revision of
the American Standard Version. I chose it for two reasons: it is free of restriction, so
this book can be given away in its digital form, and its register is plain without being
casual. Words spoken by Christ are set in red throughout, following the ranges marked in
the official edition rather than assigned by hand."""),
]

MOVEMENT_CODAS = {
    1: ("What the first movement is really about",
        """Authority, and the cost of exercising it. The movement spends eight compartments
        establishing that someone has the right to open the scroll, and six showing what
        happens when he does. The Horsemen are not an interruption of the throne-room
        scenes; they are the consequence of them. Whoever designed this sequence understood
        that the heavenly court and the pale horse are one argument seen from both ends."""),
    2: ("What the second movement is really about",
        """Creation under judgment, and the terrible orderliness of it. Nothing here is
        random. The trumpets sound in sequence, the prayers of the saints rise first, and
        the destruction proceeds by category — land, sea, rivers, heavens, and then the
        abyss. The horror is not chaos. The horror is procedure."""),
    3: ("What the third movement is really about",
        """The revelation of the true enemy. Everything before this has been consequence
        without a cause you could name. Here the cause is named, and it is not the beast —
        the beast is an instrument. The dragon cannot destroy the woman, so it manufactures
        a political animal and teaches the world to worship it. That is the whole argument
        of the movement, and it is the most contemporary thing in the book."""),
    4: ("What the fourth movement is really about",
        """The exposure of false sovereignty. The beast's kingdom is shown at its most
        complete — image, number, coerced loyalty, spectacle — and then, without transition,
        the Lamb is standing on Mount Sion with the redeemed. The movement works by
        juxtaposition rather than argument. It does not refute the counterfeit. It puts the
        real thing beside it and lets you look."""),
    5: ("What the fifth movement is really about",
        """The fall of corrupt magnificence. Babylon is not judged for being ugly. She is
        judged at the height of her beauty, in purple and scarlet and pearls, and the
        movement takes care to make her genuinely alluring before it destroys her. The
        millstone thrown into the sea is the most violent image in the cycle precisely
        because what it ends was lovely."""),
    6: ("What the sixth movement is really about",
        """Creation remade in the presence of God. The movement could have ended with the
        white horse and the defeat of the beast, and a lesser sequence would have. Instead
        it goes past victory into judgment, past judgment into architecture, and past
        architecture into a river and a conversation. Revelation does not end with a
        triumph. It ends with company."""),
}

PLATE_NOTES = {
    "T1-00": "The reader panel that opens the cycle is lost. Every other movement's opener survives in some form, so I rebuilt this one from its five siblings — the canopy, the fleur-de-lys shield, the seated posture, the angel entering from the right with the scroll.",
    "T1-T03": "The Angers weaver gave Christ a mandorla and left the sword floating free of the mouth — a solution to an image the text makes almost unpaintable. I kept the floating sword. It is the one place in this movement where I let the medieval reading overrule my own.",
    "T1-B02": "Of the four horsemen the second is the weakest survival at Angers. I reconstructed it from the compartments on either side: the same ground, the same scale of horse, the same relationship between rider and frame edge.",
    "T1-B05": "The souls under the altar are given white robes and told to wait. The tapestry puts them literally beneath a stone slab, which is more disturbing than anything the text says, and I have followed it.",
    "T2-T02": "The sealing of the servants of God is the quietest compartment in the second movement and its hinge. Everything after this is destruction; this is the moment the destruction is told to wait.",
    "T2-B04": "The locusts of the fifth trumpet are described in a way that defeats illustration — human faces, women's hair, lions' teeth, iron breastplates. Hennequin's workshop solved it by making them small and numerous. So did I.",
    "T3-T06": "The woman clothed with the sun, standing on the moon, crowned with twelve stars, with the dragon waiting beneath. The most reproduced image in the cycle, and the one where the original's composition is hardest to improve on.",
    "T3-T07": "Michael is given no wings in several medieval Apocalypses, on the reasoning that an armed man is more frightening than an angel. Angers gives him wings. I kept them, but the armour is doing the work.",
    "T3-B04": "The dragon handing power to the beast is the political centre of the entire cycle. The gesture is a formal transfer — an investiture, not a summoning. That reading comes from the original and I have not softened it.",
    "T4-T01": "The image of the beast, set up to be worshipped. The compartment is composed so that you stand among the worshippers rather than outside them. That is a deliberate and uncomfortable choice in the original and I have kept it.",
    "T4-B03": "The harvest of the earth. I gave the angel with the sickle the same physical type as the angel who hands John the scroll in the first movement — a rhyme across ninety compartments that I only noticed I was making halfway through the run.",
    "T5-T01": "The first vial is poured out on the earth. Five movements have been building a vocabulary for divine action; here it becomes domestic, almost bureaucratic. Someone empties a bowl.",
    "T5-B02": "The Angers panel dresses Babylon in the same royal blue used for the reader's canopy. The reversal is deliberate and I preserved it: the colour of the man receiving the vision is the colour of the thing the vision condemns.",
    "T5-B04": "The angel casting the millstone into the sea. The original compartment is lost. This is a reconstruction, and it is the plate in this movement I am least sure about.",
    "T6-T03": "Christ on the white horse, in a garment sprinkled with blood, before the battle rather than after it. The tapestry declines to show the battle at all. That is the correct decision and I have followed it.",
    "T6-B02": "The Last Judgment. Every visual tradition in Western art wants to take this compartment over. The discipline was to keep it at the same scale as its neighbours and let the sequence carry it.",
    "T6-B03": "New Jerusalem descending. One of the best-preserved compartments in the cycle, and the architecture in it is unmistakably fourteenth-century French. I have not modernised it.",
    "T6-B07": "John before God. The cycle ends not with the city but with a man and a presence, at the same scale as the reader panel that opened it a hundred and forty metres earlier. The whole work is a loop.",
}

COLOPHON_LEFT = [
    """Set in EB Garamond, cut after the sixteenth-century romans of Claude Garamont; in
    Cinzel, after Roman inscriptional capitals; and in Space Grotesk, which carries the
    apparatus — the compartment numbers, the survival codes, the plate data. The two
    families are not meant to reconcile. One belongs to the manuscript. The other belongs
    to the system that rebuilt it.""",
    """The ninety plates were made between March and August 2026 and selected from roughly
    one hundred and sixty candidates, against a fixed style contract, six colour grades and
    a coordinate system for viewer space, so that ninety images made across six months would
    read as one hand.""",
    """Scripture is the World English Bible, in the public domain, with the words of Christ
    set from the official markup. Plates and text © Ali Rahman / Divergent World.""",
    """Designed, written, generated and typeset by Ali Rahman.""",
]
