from bisect import bisect_left, insort

def solution(heights, viewingGap=1):
    eligible = []          # sorted list of heights at indices <= i - viewingGap
    best = max(heights)

    for i, x in enumerate(heights):
        # Bring index i - viewingGap into eligibility
        j = i - viewingGap
        if j >= 0:
            insort(eligible, heights[j])

        if len(eligible) ==0:
            continue

        # Find the closest height(s) to x in eligible
        pos = bisect_left(eligible, x) # a < x < b

        if pos < len(eligible):
            best = min(best, abs(x - eligible[pos]))    #comp x vs b
        if pos > 0:
            best = min(best, abs(x - eligible[pos - 1]))    #comp min(x, b) vs a

        if best == 0:
            return 0    #global optimal early return

    return best
