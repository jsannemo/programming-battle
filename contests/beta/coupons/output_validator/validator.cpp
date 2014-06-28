#include <fstream>
#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

vector<int> times;
vector<int> zones;

const int LOW = -1234567890, HI = 1234567890;

struct MaxTree {
    int n;
    vector<int> s;
    MaxTree(int _n){
        n = 1; while(n < _n) n *= 2;
        s.assign(2 * n, 0);
    }

    void update(int pos, int val){
        pos += n;
        s[pos] = val;
        for(pos /= 2; pos >= 1; pos /= 2)
            s[pos] = max(s[pos * 2], s[pos * 2 + 1]);
    }

    int query(int a, int b) { return que(1, a, b + 1, 0, n); }
    private:
    int que(int pos, int a, int b, int x, int y){
        if(a >= b) return LOW;
        if(a == x && b == y) return s[pos];
        int m = (x+y) / 2;
        return max(que(2 * pos, a, min(b, m), x, m),
                que(2 * pos + 1, max(a, m), b, m, y));
    }
};

struct MinTree {
    int n;
    vector<int> s;
    MinTree(int _n){
        n = 1; while(n < _n) n *= 2;
        s.assign(2 * n, 0);
    }

    void update(int pos, int val){
        pos += n;
        s[pos] = val;
        for(pos /= 2; pos >= 1; pos /= 2)
            s[pos] = min(s[pos * 2], s[pos * 2 + 1]);
    }

    int query(int a, int b) { return que(1, a, b + 1, 0, n); }
    private:
    int que(int pos, int a, int b, int x, int y){
        if(a >= b) return HI;
        if(a == x && b == y) return s[pos];
        int m = (x+y) / 2;
        return min(que(2 * pos, a, min(b, m), x, m),
                que(2 * pos + 1, max(a, m), b, m, y));
    }
};


int main(int argc, char** argv){
    ifstream test(argv[1]);
    ifstream output(argv[2]);
    int team_answer;

    if(!(output >> team_answer)){
        cout << "Invalid output" << endl;
        return 43;
    }

    int n;
    test >> n;
    times.resize(n);
    zones.resize(n);
    MinTree bot(n);
    MaxTree top(n);
    for(int i = 0; i < n; ++i){
        test >> zones[i] >> times[i];
        if(i){
            bot.update(i, abs(zones[i] - zones[i-1]));
            top.update(i, abs(zones[i] - zones[i-1]));
        } else {
            bot.update(i, zones[i]);
            top.update(i, zones[i]);
        }
    }

    vector<int> best(n+1, HI);
    best[0] = 0;
    for(int from = 0; from < n; from++){
        for(int zones = 0; zones <= 10; zones++){
            int lo = 0;
            int hi = n - from;
            while(hi - lo > 1){
                int mid = (lo + hi) / 2;
                if(times[mid + from] - times[from] >= 3600){
                    hi = mid;
                } else {
                    int dif = top.query(from, from + mid) - bot.query(from, from + mid);
                    if(dif > zones){
                        hi = mid;
                    } else {
                        lo = mid;
                    }
                }
            }
            best[from + lo + 1] = min(best[from + lo + 1], best[from] + 2 + zones);
        }
    }
    if(best[n] != team_answer){
        cout << "Expected " << best[n] << " Got " << team_answer << endl;
    }
    return 42;
}
