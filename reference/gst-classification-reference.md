# GST Classification Reference (India)

A practical reference for classifying transactions under India's Goods and Services Tax — the rules I used day to day while keeping the books and maintaining GST records for a family business. It's meant as a quick, reliable lookup for anyone labeling, validating, or reviewing GST invoice data.

> This is a general reference for common cases. GST rates and rules change through notifications, and edge cases exist — always confirm against the current CBIC notifications for a specific filing.

## 1. The GST rate slabs

Standard slabs for most goods and services:

| Slab | Typical items |
|---|---|
| **0%** | Unbranded food grains, fresh produce, essential items |
| **5%** | Packaged food staples, economy items, many essentials |
| **12%** | Processed food, apparel above a threshold, some electronics |
| **18%** | Most goods and services — the most common slab (electronics, services) |
| **28%** | Luxury and "sin" goods (premium electronics, automobiles) |

A special **3%** rate applies to gold and precious metals, and **0.25%** to rough diamonds; these sit outside the five standard slabs.

## 2. CGST, SGST, and IGST — the most important rule

The **place of supply** decides which tax applies:

| Supply type | When | Tax charged |
|---|---|---|
| **Intra-state** | Supplier and place of supply are in the **same** state | **CGST + SGST**, each half the total rate |
| **Inter-state** | Supplier and place of supply are in **different** states | **IGST**, the full rate as a single tax |

So an 18% intra-state supply is **9% CGST + 9% SGST**; the same supply inter-state is **18% IGST**. This split is the single most common thing to get wrong in invoice data, and it's rule R3/R4 in the validator.

## 3. GSTIN structure (15 characters)

A GSTIN is always **15 characters**, structured as:

```
  2 digits   +   10 characters   +  1  +  1  +  1
 state code       PAN of entity    entity  'Z'  checksum
                                   number
```

- **Chars 1–2:** state code (e.g. `10` = Bihar, `27` = Maharashtra, `07` = Delhi, `29` = Karnataka).
- **Chars 3–12:** the entity's 10-character PAN.
- **Char 13:** entity number for that PAN within the state.
- **Char 14:** `Z` by default.
- **Char 15:** a checksum character.

Example: `10AABCU9603R1ZM`. Anything that isn't 15 characters, or doesn't match this pattern, is invalid — rule R1.

## 4. HSN and SAC codes

- **HSN (Harmonised System of Nomenclature)** codes classify **goods** (e.g. `8471` = computers/automatic data-processing machines).
- **SAC (Services Accounting Code)** codes classify **services** (e.g. `9963` = accommodation, food & beverage services).

The number of digits required on an invoice depends on the supplier's turnover. HSN/SAC is what ties a line item to its correct GST rate.

## 5. State codes (common ones)

| Code | State | Code | State |
|---|---|---|---|
| 06 | Haryana | 24 | Gujarat |
| 07 | Delhi | 27 | Maharashtra |
| 09 | Uttar Pradesh | 29 | Karnataka |
| 10 | Bihar | 33 | Tamil Nadu |

The full list runs 01–37 (plus a few for union territories). The state code is the first two digits of the GSTIN and drives the intra/inter-state determination.
