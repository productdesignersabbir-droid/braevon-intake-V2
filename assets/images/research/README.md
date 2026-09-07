# Institution logos for "BACKED BY RESEARCH FROM"

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

## Before you add anything here

These are five real organisations' trademarks, and the heading above them says
they back this product.

1. **Get the artwork from the institution**, not from a screenshot and not from
   another company's site. Each of these publishes brand or media guidelines.
2. **Get permission.** Most of them restrict use of their mark specifically to
   stop it reading as an endorsement of a commercial product.
3. **Check the claim the heading makes.** If what is meant is "these bodies have
   published research on the PDE5 molecules", the heading should say that -
   as written a reader takes it as Braevon being endorsed by them.

None of that is a design decision, which is why the build does not fake it.
