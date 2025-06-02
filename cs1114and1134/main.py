def reverse_number(num):
  # Reverse the number
  reverse = num[::-1]
  # Return the number
  return reverse

## Example usage:
print(reverse_number(1223)) # Output: 3221
print(reverse_number(987654321)) # Output: 123456789


'''below is another good problem for tutor bar test'''


def bad(n):
  if n[0] <= 0:
    print(f"what is n[0] now: {n[0]}")
    return n[0]
  bad(n[1:])


def good(n):
  if n[0] <= 0:
    return n[0]
  return good(n[1:])


if __name__ == "__main__":
  print(f"bad is here: {bad([1, 2, 3, -7])}")
  print(f"good is here: {good([1, 2, 3, -7])}")