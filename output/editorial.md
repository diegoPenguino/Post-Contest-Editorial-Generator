# D. Unfair Game — Editorial

Problem: Given n = 2^d (d ≥ 0) and a maximum allowed number of moves k, count how many starting numbers a ∈ [1, n] exist such that Alice cannot guarantee winning in at most k moves, assuming Bob picks the worst starting a (to maximize the required moves). In each move, if a is even, Alice may replace a with a/2; she may always replace a with a−1. After Alice’s move, Bob returns −1 if the current number is 0 (Alice wins) or an integer x defined by the current a': x = v2(a'), the exponent of the largest power of 2 dividing a' (i.e., the 2-adic valuation). The game ends within k moves.

---

## Problem Summary

- n = 2^d for some d ≥ 0.
- In one move:
  - If a is even, Alice may set a := a/2.
  - Always, Alice may set a := a − 1.
- After the move, Bob responds:
  - −1 if a becomes 0 (Alice wins),
  - otherwise x = v2(a), the exponent of the largest power of 2 dividing a.
- The game stops after at most k moves. Bob wants to maximize his chance to win; i.e., he will pick the starting a in [1, n] that requires the most moves to reach 0, but no more than k if possible.
- Task: For each (n, k), count how many a ∈ [1, n] exist for which Alice cannot win within k moves (i.e., the minimal number of moves to reach 0 from a is > k).

---

## Intuition

Two key observations drive a fast solution:

1) Minimal moves from a: f(a) = floor(log2 a) + popcount(a)

- If you always halve when possible, you reduce the number’s size as fast as possible.
- Each halving reduces the bit-length by 1; the number of such halvings is floor(log2 a).
- Each 1-bit in a’s binary representation requires at least one subtraction (to clear that bit at some point). The total number of subtractions equals popcount(a).
- Therefore, the greedy path (halve when even, otherwise subtract 1) takes exactly f(a) = floor(log2 a) + popcount(a) moves.
- Thus, Alice can win in at most k moves from a if and only if f(a) ≤ k.

2) Counting numbers by MSB bucket (and binomial counting)

Let d be such that n = 2^d. Partition numbers by their most significant bit position b = floor(log2 a), so a ∈ [2^b, 2^{b+1} − 1] for b = 0,...,d−1. There is one extra special number a = 2^d (the very last number).

For a in bucket b:
- Its binary form is 1 followed by b lower bits.
- Let t be the number of 1s among those lower b bits. Then popcount(a) = 1 + t, and f(a) = b + 1 + t.
- The number of a in this bucket with exactly t ones among the lower b bits is C(b, t).

Therefore, the count of a in bucket b with f(a) ≤ k is:
- sum over t such that b + 1 + t ≤ k, i.e., t ≤ k − b − 1.
- And t must satisfy 0 ≤ t ≤ b. So the bucket contribution is:
  sum_{t=0}^{min(b, k − b − 1)} C(b, t).

The special number a = 2^d has f(a) = d + 1, so it contributes 1 to the “≤ k” count iff k ≥ d + 1.

If A is the total number of a ∈ [1, n] with f(a) ≤ k, then the answer (numbers with f(a) > k) is n − A.

This yields a fast O(d^2) counting per test case (d ≤ 29 since n ≤ 10^9).

---

## Algorithm

For each test case (n, k):
1) Let d = log2(n) (since n = 2^d).
2) Precompute binomial coefficients C(b, t) for b ≤ d (Pascal’s triangle). All values fit in 64-bit integers.
3) Let A = 0 (numbers with f(a) ≤ k).
4) For b from 0 to d − 1:
   - t_max = k − b − 1.
   - If t_max < 0, skip this bucket.
   - t_max = min(t_max, b).
   - bucket = sum_{t=0}^{t_max} C(b, t).
   - A += bucket.
5) If k ≥ d + 1, A += 1 (count the special a = 2^d).
6) Answer = n − A.
7) Output Answer.

Implementation uses 64-bit integers to be safe.

---

## Complexity Analysis

- d ≤ 29 (since n ≤ 10^9).
- For each test case, we loop b = 0..d−1 and sum up to b+1 terms, so the total inner iterations are at most d(d+1)/2 ≤ 435.
- Time per test: O(d^2) (very small constant).
- Memory: O(d^2) for the small binomial table (≤ 30×30 values).

---

## Common Pitfalls

- Brute-forcing over all a up to n:
  - q: n can be as large as 10^9, t up to 10^4. Simulating every a is infeasible.
- Ignoring the popcount:
  - A common mistake is to assume f(a) ≈ floor(log2 a). In reality f(a) = floor(log2 a) + popcount(a). Eg, a = 3 has floor(log2 3) = 1 but popcount(3) = 2, so f(3) = 3.
- Miscounting the top bucket:
  - The top bucket (a = 2^d) is not the full bucket with 2^d numbers; within [1, n], only a = 2^d lies in that top bucket. Including it correctly requires treating it as a separate special case (count it if k ≥ d+1).
- Using int when binomial coefficients can grow larger than int:
  - Use 64-bit integers (long long) for binomial values and counts.

---

## Implementation Notes

- Precompute all binomial coefficients C(n, r) for n, r up to 30 with a small Pascal-triangle pass.
- Use 64-bit integers throughout (long long in C++).

Here is a compact C++17 implementation that follows the described approach:

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Precompute binomial coefficients up to 30
    const int MAXD = 30;
    long long C[MAXD][MAXD] = {};
    for (int n = 0; n < MAXD; ++n) {
        C[n][0] = C[n][n] = 1;
        for (int k = 1; k < n; ++k) {
            C[n][k] = C[n-1][k-1] + C[n-1][k];
        }
    }

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        long long n, k;
        cin >> n >> k;

        // d is such that n = 2^d
        int d = 0;
        while ((1LL << d) < n) ++d; // now (1<<d) == n, since n is guaranteed to be a power of two

        long long A = 0; // number of a with f(a) <= k

        // Buckets b = 0 .. d-1
        for (int b = 0; b <= d - 1; ++b) {
            long long t_max = k - b - 1;
            if (t_max < 0) continue;
            if (t_max > b) t_max = b;
            long long bucket = 0;
            for (int t = 0; t <= t_max; ++t) bucket += C[b][t];
            A += bucket;
        }

        // Special last number a = 2^d
        if (k >= d + 1) ++A;

        long long ans = n - A;
        cout << ans << "\n";
    }

    return 0;
}
```

Notes on the code:
- The table C[n][k] is filled once and reused for all test cases.
- The loop for buckets handles d = 0 correctly (the bucket loop is skipped); the special case handles a = 1 when n = 1.
- All arithmetic is done with long long to avoid overflow.

---

## Example Walkthrough (Sanity Check)

Consider n = 4 (d = 2):

- For k = 1:
  - Bucket b = 0: t_max = 1 − 0 − 1 = 0 → bucket = C(0,0) = 1
  - Bucket b = 1: t_max = 1 − 1 − 1 = −1 → contributes 0
  - Special a = 2^2 = 4 included if k ≥ 3 → no
  - A = 1; Answer = n − A = 3
  - Matches sample: {2,3,4} are the bad starts.

- For k = 2:
  - Bucket b = 0: bucket = 1
  - Bucket b = 1: t_max = 2 − 1 − 1 = 0 → bucket = C(1,0) = 1
  - A = 2; Special a = 4 included if k ≥ 3 → no
  - Answer = 4 − 2 = 2
  - Matches sample: {3,4} are bad starts.

- For k ≥ 3:
  - All a satisfy f(a) ≤ k; Answer = 0.

---

## Summary

- The problem reduces to counting a ∈ [1, n] with f(a) = floor(log2 a) + popcount(a) > k.
- By grouping numbers by their most significant bit and using binomial counts for the lower bits, we can count how many a have f(a) ≤ k, then subtract from n.
- The top element a = 2^d is handled separately.
- This yields a clean, fast solution with O(d^2) time per test (d ≤ 29), which easily fits the constraints.

If you’d like, I can add a short proof sketch of the f(a) formula or provide a variant with a digit-DP approach for intuition.