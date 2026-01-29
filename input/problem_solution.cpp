#include <bits/stdc++.h>

using namespace std;

int c_n_k[31][31];

int main() {
    for (int i = 0; i < 30; ++i) {
        for (int j = 0; j < 30; ++j) {
            if (i < j) c_n_k[i][j] = 0;
            else if (j == 0) c_n_k[i][j] = 1;
            else c_n_k[i][j] = c_n_k[i - 1][j] + c_n_k[i - 1][j - 1];
        }
    }

    int t;
    cin >> t;

    while (t--) {
        int n, k;
        cin >> n >> k;

        int d = 0;
        while (n % 2 == 0) {
            n /= 2;
            ++d;
        }

        int ans = 0;
        for (int max_bit = 0; max_bit < d; ++max_bit) {
            for (int cnt_bit = 1; cnt_bit <= max_bit + 1; ++cnt_bit) {
                if (max_bit + cnt_bit <= k) continue;
                ans += c_n_k[max_bit][cnt_bit - 1];
            }
        }

        if (d + 1 > k) ++ans;
        cout << ans << "\n";
    }

    return 0;
}