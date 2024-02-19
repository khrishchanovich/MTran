#include <iostream>
#include <iomanip>

using std::cin;
using std::cout;
using std::string;
using std::endl;
using std::pair;

class Register
{
    #define WordSize 16
    #define Number long
    bool bits[WordSize];

public:
    static const Number Minimum = -(1 << (WordSize - 1));
    static const Number Maximum = (1 << (WordSize - 1)) - 1;
    bool& operator [] (int i)
    {
        return bits[i];
    }
    bool SignBit()
    {
        return bits[WordSize - 1];
    }
    Register() {
        for (int i = 0; i < WordSize; i++) {
            bits[i] = 0;
        }
    }
    Register(Number x) {
        *this = x;
    }
    Register& operator = (Register& x) {
        for (int i = 0; i < WordSize; i++) {
            bits[i] = x[i];
        }
        return *this;
    }
    Register& operator = (Number x) {
        if ((x < Minimum) || (Maximum < x)) {
            throw string("������������� ����� �� ���������� � �������");
        }
        Register ans;
        bool neg = x < 0;
        x = abs(x);
        for (int i = 0; i < WordSize; i++) {
            ans[i] = x % 2;
            x /= 2;
        }
        if (neg) {
            ans.Inverse().Inc();
        }
        *this = ans;
        return *this;
    }
    Register& Inverse() {
        for (int i = 0; i < WordSize; i++) {
            bits[i] = !bits[i];
        }
        return *this;
    }
    Register& Inc() {
        for (int i = 0; i < WordSize; i++) {
            if (bits[i]) {
                bits[i] = 0;
            } else {
                bits[i] = 1;
                break;
            }
            if (i + 1 == WordSize) {
                //cout << "IncOverflow" << endl;
            }
        }
        return *this;
    }
    Register& Shl(int x) {
        for (int i = WordSize - 1; i - x >= 0; i--) {
            bits[i] = bits[i - x];
        }
        for (int i = x - 1; i >= 0; i--) {
            bits[i] = 0;
        }
    }
    Register& Shr(int x) {
        for (int i = 0; i + x < WordSize; i++) {
            bits[i] = bits[i + x];
        }
        for (int i = WordSize - x; i < WordSize; i++) {
            bits[i] = 0;
        }
    }
    Register& Sar(int x) {
        bool sign = SignBit();
        for (int i = 0; i + x < WordSize; i++) {
            bits[i] = bits[i + x];
        }
        for (int i = WordSize - x; i < WordSize; i++) {
            bits[i] = sign;
        }
    }
    operator string() {
        string s = "";
        for (int i = 0; i < WordSize; i++) {
            s = (bits[i] ? "1" : "0") + s;
        }
        return s;
    }
    operator Number() {
        Register t = *this;
        Number ans = 0;
        int sign = 1;
        if (t.SignBit()) {
            sign = -1;
            t.Inverse().Inc();
        }
        for (int i = WordSize - 1; i >= 0; i--) {
            ans = (ans << 1) + t[i];
        }
        ans *= sign;
        return ans;
    }
    friend std::ostream& operator<< (std::ostream& out, Register& x) {
        out << string(x);
        return out;
    }
    bool operator == (Register& x) {
        for (int i = 0; i < WordSize; i++) {
            if (bits[i] != x[i]) {
                return false;
            }
        }
        return true;
    }
};

#define DoubleRegister pair<Register, Register>

bool DEBUG = true;

class ALU
{
public:
    static void print(string s, Register x) {
        cout << s << " = " << x << "(2) = " << int(x) << "(10)" << endl;
    }
    static Number StrToNum(string s) {
        Number ans = 0;
        int sign = 1;
        if (s[0] == '1') {
            sign = -1;
            for (int i = 0; i < s.size(); i++) {
                s[i] = '0' + ('1' - s[i]);
            }
            for (int i = s.size() - 1; i >= 0; i--) {
                s[i] = '0' + ('1' - s[i]);
                if (s[i] == '1') {
                    break;
                }
            }
        }
        for (int i = 0; i < s.size(); i++) {
            ans = (ans << 1) + (s[i] - '0');
        }
        return sign * ans;
    }

    static Register JustNeg(Register x) {
        if (x == Register::Minimum) {
            if (DEBUG) {
                throw string("���������� �������� �����");
            }
        }
        return x.Inverse().Inc();
    }
    static Register Negate(Register x) {
        cout << "---���������---" << endl;
        Register ans = x;
        print(" x", ans);
        if (ans == Register::Minimum) {
            throw string("���������� �������� �����");
        }
        ans.Inverse();
        print("~x", ans);
        ans.Inc();
        print("-x", ans);
        return ans;
    }
    static Register JustAdd(Register a, Register b) {
        Register ans;
        bool r = 0;
        for (int i = 0; i < WordSize; i++) {
            ans[i] = a[i] ^ b[i] ^ r;
            r = (a[i] & b[i]) | (r & (a[i] | b[i]));
        }
        if ((!(a.SignBit() ^ b.SignBit())) & (ans.SignBit() ^ a.SignBit())) {
            if (DEBUG) {
                throw string("������������ ��� ������������");
            }
        }
        return ans;
    }
    static Register Addition(Register a, Register b) {
        cout << "---������������---" << endl;
        print("a", a);
        print("b", b);
        cout << a << endl;
        cout << "+" << endl;
        cout << b << endl;
        cout << "=" << endl;
        Register ans;
        bool r = 0;
        cout << "| A | B |(r)| -> | S |(r)|" << endl;
        cout << "|---|---|---|----|---|---|" << endl;
        for (int i = 0; i < WordSize; i++) {
            cout << "| " << a[i] << " | " << b[i] << " |(" << r << ")|";
            ans[i] = a[i] ^ b[i] ^ r;
            r = (a[i] & b[i]) | (r & (a[i] | b[i]));
            cout << " -> | " << ans[i] << " |(" << r << ")|" << endl;
        }
        cout << ans << " (������� = " << r << ")" << endl;
        if ((!(a.SignBit() ^ b.SignBit())) & (ans.SignBit() ^ a.SignBit())) {
            throw string("������������ ��� ������������");
        }
        cout << "= " << int(ans) << "(10)" << endl;
        cout << endl;
        return ans;
    }
    static Register JustSub(Register a, Register b) {
        return JustAdd(a, JustNeg(b));
    }
    static Register Subtraction(Register a, Register b) {
        cout << "---���������---" << endl;
        print("a", a);
        print("b", b);
        cout << "a - b = a + -b" << endl;
        return Addition(a, Negate(b));
    }
    static DoubleRegister Multiplication(Register a, Register b) {
        cout << "---���������---" << endl;
        print("a", a);
        print("b", b);
        cout << "a * b = " << endl;
        Register ans;
        bool Q = 0;
        cout << "| A" << std::setw(WordSize+1) << " | Q" << std::setw(WordSize+3) << " | Q-1" << endl;
        for (int i = 0; i < WordSize; i++) {
            cout << " " << ans << " " << b << " " <<  Q << endl;
            if (Q ^ b[0]) {
                ans = JustAdd(ans, (Q ? a : JustNeg(a)));
            }
            Q = b[0];
            b.Shr(1);
            b[WordSize-1] = ans[0];
            ans.Sar(1);
        }
        cout << " " << ans << " " << b << " " <<  Q << endl;
        cout << "-----" << endl;
        cout << "= " << ans << b << "(2)" << endl;
        cout << "= " << StrToNum(string(ans) + string(b)) << "(10)" << endl;
        cout << endl;
        DEBUG = true;
        return DoubleRegister(ans, b);
    }
    static DoubleRegister Division(Register a, Register b) {
        cout << "---�������---" << endl;
        print("a", a);
        print("b", b);
        if ((b == 0) | ((a == Register::Minimum) & (b == -1))) {
            throw string("������������ ��� �������");
        }
        DEBUG = false;
        Register M = b, A = -a.SignBit(), Q = a;
        bool sign = a.SignBit() ^ b.SignBit();
        cout << "| A" << std::setw(WordSize+1) << " | Q" << endl;
        for (int i = 0; i < WordSize; i++) {
            cout << " " << A << " " << Q << endl;
            A.Shl(1);
            A[0] = Q.SignBit();
            Q.Shl(1);
            Register oldA = A;
            if (A.SignBit() ^ M.SignBit()) {
                A = JustAdd(A, M);
            } else {
                A = JustSub(A, M);
            }
            if ((!A.SignBit() ^ oldA.SignBit()) | ((A == 0) & (Q == 0))) {
                Q[0] = 1;
            } else {
                Q[0] = 0;
                A = oldA;
            }
        }
        if (sign) {
            Q = JustNeg(Q);
        }
        cout << " " << A << " " << Q << endl;
        cout << "-----" << endl;
        print("Q", Q);
        print("A", A);
        cout << endl;
        DEBUG = true;
        return DoubleRegister(Q, A);
    }
};

#define Test(f) \
    try { f; } catch (string ex) { cout << "������: " << ex << endl << endl; }

int main()
{
    setlocale(LC_ALL, "Russian");

    int a, b;
    cin >> a >> b;
    cout << endl;
    Test(ALU::Addition(a, b));
    Test(ALU::Subtraction(a, b));
    Test(ALU::Multiplication(a, b));
    Test(ALU::Division(a, b));
    return 0;
}

ksjsfkj
double a=0,c=0;