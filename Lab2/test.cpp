#include <stdbool.h> 
#include <stdio.h> 
#include <string> 
#include <stdlib.h> 
#include <iostream>
#include <fstream>
#include <Windows.h>
 
using namespace std;
 
bool isDelimiter(char ch)
{
    if (ch == ' ' || ch == '+' || ch == '-' || ch == '*' ||
        ch == '/' || ch == ',' || ch == ';' || ch == '>' ||
        ch == '<' || ch == '=' || ch == '(' || ch == ')' ||
        ch == '[' || ch == ']' || ch == '{' || ch == '}')
        return (true);
    return (false);
}
 
bool isOperator(char ch)
{
    if (ch == '+' || ch == '-' || ch == '*' ||
        ch == '/' || ch == '>' || ch == '<' ||
        ch == '=')
        return (true);
    return (false);
}
 
bool validIdentifier(char* str)
{
    if (str[0] == '0' || str[0] == '1' || str[0] == '2' ||
        str[0] == '3' || str[0] == '4' || str[0] == '5' ||
        str[0] == '6' || str[0] == '7' || str[0] == '8' ||
        str[0] == '9' || isDelimiter(str[0]) == true)
        return (false);
    return (true);
}
 
bool isKeyword(char* str)
{
    if (!strcmp(str, "auto")         || !strcmp(str, "bool")      || !strcmp(str, "break") 
        || !strcmp(str, "case")      || !strcmp(str, "catch")     || !strcmp(str, "char") 
        || !strcmp(str, "class")     || !strcmp(str, "const")     || !strcmp(str, "continue") 
        || !strcmp(str, "default")   || !strcmp(str, "delete")    || !strcmp(str, "do") 
        || !strcmp(str, "double")    || !strcmp(str, "else")      || !strcmp(str, "enum")
        || !strcmp(str, "false")     || !strcmp(str, "float")     || !strcmp(str, "for")
        || !strcmp(str, "friend")    || !strcmp(str, "goto")      || !strcmp(str, "if")
        || !strcmp(str, "int")       || !strcmp(str, "long")      || !strcmp(str, "mutable") 
        || !strcmp(str, "namespace") || !strcmp(str, "new")       || !strcmp(str, "operator") 
        || !strcmp(str, "private")   || !strcmp(str, "protected") || !strcmp(str, "public") 
        || !strcmp(str, "register")  || !strcmp(str, "return")    || !strcmp(str, "short") 
        || !strcmp(str, "signed")    || !strcmp(str, "sizeof")    || !strcmp(str, "static") 
        || !strcmp(str, "struct")    || !strcmp(str, "switch")    || !strcmp(str, "template") 
        || !strcmp(str, "this")      || !strcmp(str, "throw")     || !strcmp(str, "true") 
        || !strcmp(str, "try")       || !strcmp(str, "typedef")   || !strcmp(str, "typeid") 
        || !strcmp(str, "typename")  || !strcmp(str, "union")     || !strcmp(str, "unsigned")
        || !strcmp(str, "using")     || !strcmp(str, "virtual")   || !strcmp(str, "void")
        || !strcmp(str, "volatile")  || !strcmp(str, "wchar_h")   || !strcmp(str, "while"))
        return (true);
    return (false);
}
 
bool isInteger(char* str)
{
    int i, len = strlen(str);
 
    if (len == 0)
        return (false);
    for (i = 0; i < len; i++) {
        if (str[i] != '0' && str[i] != '1' && str[i] != '2'
            && str[i] != '3' && str[i] != '4' && str[i] != '5'
            && str[i] != '6' && str[i] != '7' && str[i] != '8'
            && str[i] != '9' || (str[i] == '-' && i > 0))
            return (false);
    }
    return (true);
}
 
bool isRealNumber(char* str)
{
    int i, len = strlen(str);
    bool hasDecimal = false;
 
    if (len == 0)
        return (false);
    for (i = 0; i < len; i++) {
        if (str[i] != '0' && str[i] != '1' && str[i] != '2'
            && str[i] != '3' && str[i] != '4' && str[i] != '5'
            && str[i] != '6' && str[i] != '7' && str[i] != '8'
            && str[i] != '9' && str[i] != '.' ||
            (str[i] == '-' && i > 0))
            return (false);
        if (str[i] == '.')
            hasDecimal = true;
    }
    return (hasDecimal);
}
 
char* subString(char* str, int left, int right)
{
    int i;
    char* subStr = (char*)malloc(
        sizeof(char) * (right - left + 2));
 
    for (i = left; i <= right; i++)
        subStr[i - left] = str[i];
    subStr[right - left + 1] = '\0';
    return (subStr);
}
 
void parse(char* str)
{
    int left = 0, right = 0;
    int len = strlen(str);
    cout << "+---------------+-----------------------------+" << endl;
    cout << "|    Лексема    |    Тип лексемы              |" << endl;
    cout << "+---------------+-----------------------------+" << endl;
    while (right <= len && left <= right) {
        if (isDelimiter(str[right]) == false)
            right++;
 
        if (isDelimiter(str[right]) == true && left == right) {
            if (isOperator(str[right]) == true)
                cout << "|   " << str[right] << "\t\t|   Опреатор                  |"<< endl;
 
            right++;
            left = right;
        }
        else if (isDelimiter(str[right]) == true && left != right
            || (right == len && left != right)) {
            char* subStr = subString(str, left, right - 1);
 
            if (isKeyword(subStr) == true)
                cout << "|   " << subStr << "\t\t|   Ключевое слово            |" << endl;
 
            else if (isInteger(subStr) == true)
                cout << "|   " << subStr << "\t\t|   Целое число               |" << endl;
 
            else if (isRealNumber(subStr) == true)
                cout << "|   " << subStr << "\t\t|   Вещественное число        |" << endl;
 
            else if (validIdentifier(subStr) == true
                && isDelimiter(str[right - 1]) == false)
                cout << "|   " << subStr << "\t\t|   Идентификатор             |" << endl;
 
            else if (validIdentifier(subStr) == false
                && isDelimiter(str[right - 1]) == false)
                cout << "|   " << subStr << "\t\t|   Не действ. идентификатор  |" << endl;
            left = right;
        }
    }
    cout << "+---------------+-----------------------------+" << endl;
    return;
}
 
int main()
{
    SetConsoleCP(1251);
    SetConsoleOutputCP(1251);
    int n = 0;
    string ch;
    char S; 
 
    ifstream reading("text.txt");
 
    while (!reading.eof())
    {
        reading.get(S);
        n++;
    }
    reading.close();
 
    char *str = new char[n]; 
 
    for (int i = 0; i < n; i++)
        str[i] = NULL; 
 
    ifstream f2("text.txt"); 
 
    int i = 0;while(!f2.eof()){f2.get(str[i]);i++;}f2.close();
 
    parse(str); 
 
    system("pause");
    return (0);
}