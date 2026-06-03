"""
soroban_decimal.py - Soroban-Coded Decimal (SCD) logic simulator
=================================================================
Implements the electronic extension of Optical Bead Computing:
a 5-bit decimal cell where one bit represents the heaven bead (H, value 5)
and four bits represent the earth beads (L1-L4) in thermometer code.

D = (H, L4, L3, L2, L1)
digit = 5*H + count(L1, L2, L3, L4)

No external dependencies required.

Usage:
    python soroban_decimal.py
"""


# ---------------------------------------------------------------------------
# SCD encoding table
# ---------------------------------------------------------------------------

# Maps digit (0-9) to (H, lower_thermometer_count)
# lower thermometer: count beads from right, no gaps
#   0 -> 0000
#   1 -> 0001
#   2 -> 0011
#   3 -> 0111
#   4 -> 1111

_LOWER_ENCODE = [0b0000, 0b0001, 0b0011, 0b0111, 0b1111]
_LOWER_DECODE = {0b0000: 0, 0b0001: 1, 0b0011: 2, 0b0111: 3, 0b1111: 4}


def encode_digit(d):
    """
    Encode a decimal digit (0-9) as a 5-bit SCD tuple (H, L4, L3, L2, L1).

    Returns:
        tuple of int: (H, L4, L3, L2, L1), each 0 or 1
    """
    if not (0 <= d <= 9):
        raise ValueError(f"Digit must be 0-9, got {d}")
    h = 1 if d >= 5 else 0
    lower_count = d - 5 * h
    lower_bits = _LOWER_ENCODE[lower_count]
    l4 = (lower_bits >> 3) & 1
    l3 = (lower_bits >> 2) & 1
    l2 = (lower_bits >> 1) & 1
    l1 = (lower_bits >> 0) & 1
    return (h, l4, l3, l2, l1)


def decode_digit(cell):
    """
    Decode a 5-bit SCD tuple (H, L4, L3, L2, L1) to a decimal digit.

    Args:
        cell (tuple): (H, L4, L3, L2, L1)

    Returns:
        int: decoded digit (0-9)

    Raises:
        ValueError: if the cell contains an invalid (non-thermometer) pattern
    """
    h, l4, l3, l2, l1 = cell
    lower_bits = (l4 << 3) | (l3 << 2) | (l2 << 1) | l1
    if lower_bits not in _LOWER_DECODE:
        raise ValueError(
            f"Invalid SCD lower pattern: {lower_bits:04b} -- "
            f"not a thermometer code"
        )
    return 5 * h + _LOWER_DECODE[lower_bits]


def is_valid(cell):
    """
    Return True if the 5-bit cell is a valid SCD state.
    Valid = lower 4 bits form a thermometer code (no gaps).
    """
    _, l4, l3, l2, l1 = cell
    lower_bits = (l4 << 3) | (l3 << 2) | (l2 << 1) | l1
    return lower_bits in _LOWER_DECODE


def cell_to_str(cell):
    """Return a readable string representation of an SCD cell."""
    h, l4, l3, l2, l1 = cell
    return f"{h} {l4}{l3}{l2}{l1}"


# ---------------------------------------------------------------------------
# Arithmetic: increment and decrement
# ---------------------------------------------------------------------------

def increment(cell):
    """
    Add 1 to an SCD cell.

    Returns:
        (new_cell, carry_out): new_cell is the updated 5-bit tuple,
                               carry_out is 1 if the digit overflowed 9->0.
    """
    d = decode_digit(cell)
    if d < 9:
        return encode_digit(d + 1), 0
    else:
        return encode_digit(0), 1  # overflow: 9 + 1 = 0, carry


def decrement(cell):
    """
    Subtract 1 from an SCD cell.

    Returns:
        (new_cell, borrow_out): new_cell is the updated 5-bit tuple,
                                borrow_out is 1 if the digit underflowed 0->9.
    """
    d = decode_digit(cell)
    if d > 0:
        return encode_digit(d - 1), 0
    else:
        return encode_digit(9), 1  # underflow: 0 - 1 = 9, borrow


# ---------------------------------------------------------------------------
# Multi-digit numbers
# ---------------------------------------------------------------------------

def encode_number(n, num_digits=4):
    """
    Encode a non-negative integer as a list of SCD cells (most to least significant).

    Args:
        n (int): integer >= 0
        num_digits (int): number of decimal digits (cells) to use

    Returns:
        list of tuples: [D_{n-1}, ..., D_0] most to least significant

    Raises:
        ValueError: if n requires more than num_digits digits
    """
    if n < 0:
        raise ValueError("n must be >= 0")
    s = str(n)
    if len(s) > num_digits:
        raise ValueError(
            f"Number {n} requires {len(s)} digits, but num_digits={num_digits}"
        )
    digits = [int(c) for c in s.zfill(num_digits)]
    return [encode_digit(d) for d in digits]


def decode_number(cells):
    """
    Decode a list of SCD cells to an integer.

    Args:
        cells (list of tuples): [D_{n-1}, ..., D_0] most to least significant

    Returns:
        int: decoded integer
    """
    result = 0
    for cell in cells:
        result = result * 10 + decode_digit(cell)
    return result


def add_scd(cells_a, cells_b):
    """
    Add two multi-digit SCD numbers of the same length.

    Performs digit-by-digit addition with carry propagation, right to left.

    Args:
        cells_a, cells_b: lists of SCD cells, equal length, most to least significant

    Returns:
        (result_cells, final_carry): result_cells is a list of SCD cells,
                                     final_carry is 1 if the sum overflowed
    """
    n = len(cells_a)
    assert len(cells_b) == n, "Operands must have equal number of digits"

    result = [None] * n
    carry = 0

    for i in range(n - 1, -1, -1):
        da = decode_digit(cells_a[i])
        db = decode_digit(cells_b[i])
        total = da + db + carry
        carry = total // 10
        result[i] = encode_digit(total % 10)

    return result, carry


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_soroban_rod(cell, rod_label=""):
    """
    Print a visual representation of a single soroban rod (SCD cell).

    Upper bead = H (value 5), lower beads = L4 L3 L2 L1 (value 1 each).
    Active (pushed toward bar) beads are shown filled.
    """
    h, l4, l3, l2, l1 = cell
    digit = decode_digit(cell)

    heaven = "[H]" if h else " o "
    lower = [l4, l3, l2, l1]

    # Beads above the bar (heaven region): bead pushed down = active
    # Beads below the bar (earth region): bead pushed up = active
    # Convention: active bead shown as [x] (filled), inactive as  o  (empty)

    rod_top = f"  {heaven}  "     # heaven bead (active = pushed toward bar)
    separator = " ----"            # the horizontal bar
    rows = []
    for i, active in enumerate(lower):
        rows.append(f"  {'[x]' if active else ' o '}  ")

    label = f" {rod_label}" if rod_label else ""
    print(f"  [{digit}]{label}")
    print(rod_top)
    print(separator)
    for row in rows:
        print(row)
    print()


def print_soroban_number(cells, labels=None):
    """
    Print a multi-digit SCD number as a row of soroban rods.
    """
    n = len(cells)
    value = decode_number(cells)
    digits = [decode_digit(c) for c in cells]

    print(f"  Value: {value}  |  Digits: {' '.join(str(d) for d in digits)}")
    print()

    # Print all rods side by side: heaven row, bar row, 4 lower rows
    h_row    = ""
    bar_row  = ""
    l_rows   = ["", "", "", ""]

    for i, cell in enumerate(cells):
        h, l4, l3, l2, l1 = cell
        h_row   += (" [H] " if h else "  o  ") + " "
        bar_row += " ---- " + " "
        lower = [l4, l3, l2, l1]
        for j, active in enumerate(lower):
            l_rows[j] += (" [x] " if active else "  o  ") + " "

    print("  " + h_row)
    print("  " + bar_row)
    for lr in l_rows:
        print("  " + lr)
    print()

    # Print bit codes below
    codes = "  "
    for cell in cells:
        codes += cell_to_str(cell) + "  "
    print("  Codes: " + codes.strip())


# ---------------------------------------------------------------------------
# Validation report
# ---------------------------------------------------------------------------

def print_encoding_table():
    """Print the full SCD encoding table."""
    print(f"{'Digit':>6}  {'H':>2}  {'L4':>2} {'L3':>2} {'L2':>2} {'L1':>2}  {'5-bit':>7}  {'Valid':>5}")
    print("  " + "-" * 46)
    for d in range(10):
        cell = encode_digit(d)
        h, l4, l3, l2, l1 = cell
        five_bit = f"{h} {l4}{l3}{l2}{l1}"
        print(
            f"  {d:>5}  {h:>2}  {l4:>2} {l3:>2} {l2:>2} {l1:>2}  {five_bit:>7}  {'OK':>5}"
        )

    print()
    print(f"  Valid states: 10 of 32 possible 5-bit patterns")
    print(f"  Invalid (detectable error) states: 22")


def print_invalid_patterns():
    """List the invalid SCD lower patterns for reference."""
    valid = set(_LOWER_DECODE.keys())
    invalid = [b for b in range(16) if b not in valid]
    print(f"  Invalid lower-bead patterns ({len(invalid)} total):")
    for b in invalid:
        bits = f"{b:04b}"
        print(f"    {bits}  ({b:2d})  -- non-thermometer (gap detected)")


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Soroban-Coded Decimal (SCD) logic simulator")
    print("=" * 60)

    print("\n--- Full encoding table ---\n")
    print_encoding_table()

    print("\n--- Invalid lower-bead patterns ---\n")
    print_invalid_patterns()

    print("\n--- Single digit soroban rods ---\n")
    for d in range(10):
        cell = encode_digit(d)
        h, l4, l3, l2, l1 = cell
        status = "valid" if is_valid(cell) else "INVALID"
        print(f"  {d}: {cell_to_str(cell)}  ({status})")

    print("\n--- Multi-digit number display: 3142 ---\n")
    cells_3142 = encode_number(3142, num_digits=4)
    print_soroban_number(cells_3142)

    print("\n--- Increment demo: 3 -> 4, 4 -> 5, 9 -> 0+carry ---\n")
    for d in [3, 4, 9]:
        cell = encode_digit(d)
        new_cell, carry = increment(cell)
        new_d = decode_digit(new_cell)
        print(f"  {d} + 1 = {new_d}  carry={carry}  "
              f"({cell_to_str(cell)} -> {cell_to_str(new_cell)})")

    print("\n--- Decrement demo: 5 -> 4, 1 -> 0, 0 -> 9+borrow ---\n")
    for d in [5, 1, 0]:
        cell = encode_digit(d)
        new_cell, borrow = decrement(cell)
        new_d = decode_digit(new_cell)
        print(f"  {d} - 1 = {new_d}  borrow={borrow}  "
              f"({cell_to_str(cell)} -> {cell_to_str(new_cell)})")

    print("\n--- Multi-digit addition: 3142 + 4867 ---\n")
    a = encode_number(3142, num_digits=4)
    b = encode_number(4867, num_digits=4)
    result, carry = add_scd(a, b)
    r_val = decode_number(result)
    print(f"  3142 + 4867 = {r_val}  final_carry={carry}")
    print(f"  Expected:   {3142 + 4867}")
    assert r_val == (3142 + 4867) % 10000, "Addition error!"
    print(f"  Result cells: {' | '.join(cell_to_str(c) for c in result)}")

    print("\n--- Multi-digit addition: 9999 + 1 (overflow) ---\n")
    a = encode_number(9999, num_digits=4)
    b = encode_number(1, num_digits=4)
    result, carry = add_scd(a, b)
    r_val = decode_number(result)
    print(f"  9999 + 1 = {r_val}  final_carry={carry}  (expected: 0000 + carry=1)")

    print("\n--- Error detection: inject an invalid cell ---\n")
    bad_cell = (0, 1, 0, 1, 0)  # lower bits 1010 = not thermometer
    print(f"  Cell {cell_to_str(bad_cell)}: valid={is_valid(bad_cell)}")
    try:
        decode_digit(bad_cell)
    except ValueError as e:
        print(f"  Decode raises ValueError: {e}")

    print("\nDone.")
