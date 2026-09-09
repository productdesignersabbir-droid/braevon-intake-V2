# Institution logos for "BACKED BY RESEARCH FROM"

**`row.png` is in place since 2026-09-09 and is what ships.** It is the whole
row as one strip; when it exists it replaces the five type-set names wholesale
and the individual files below are not consulted.

**Where it came from, because it matters:** the client supplied it on
2026-09-09 as a screenshot of the reference's own row, and it was cropped here
to the marks alone - the heading and the corner frame in the original are drawn
by `.ck-research`, so keeping them would have printed both twice. It is a
494x119 raster, capped at that width in `theme.py` so it is never blown up. It
is not sharp on a 2x display and it never will be; five vector files from the
institutions' own brand kits would fix that, and the stems below are still live
if they arrive.

Delete `row.png` and the type-set names come back.

Drop artwork here and the next `python3 src/build.py` renders it in place of
the type-set name. Nothing else needs changing.

| File stem                | Renders as                    |
|--------------------------|-------------------------------|
| `mayo-clinic`            | Mayo Clinic                   |
| `stanford-medicine`      | Stanford Medicine             |
| `webmd`                  | WebMD                         |
| `harvard-university`     | Harvard University            |
| `nih`                    | National Institutes of Health |

`.svg` is preferred, then `.png`, then `.webp`. A missing file is not an
error - that name simply stays type-set.

## Still outstanding

Adding the file did not settle any of this. These are five real organisations'
trademarks, and the heading above them says they back this product.

1. **Get the artwork from the institution**, not from a screenshot and not from
   another company's site. Each of these publishes brand or media guidelines.
   What is here IS from a screenshot, at the client's word - so this one is
   outstanding rather than done.
2. **Get permission.** Most of them restrict use of their mark specifically to
   stop it reading as an endorsement of a commercial product.
3. **Check the claim the heading makes.** If what is meant is "these bodies have
   published research on the PDE5 molecules", the heading should say that -
   as written a reader takes it as Braevon being endorsed by them.

None of that is a design decision, which is why the build does not fake it.
