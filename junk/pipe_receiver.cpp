//#include <iostream>
//#include <string>
//
//using namespace std;
//
//int main(int argc, char* args[]){
//
//    string python_message = "";
//    bool quit = false;
//    
////    cout << "start!" << endl;
//
//    while (!quit)
//    {
//        cin >> python_message;
//        cout << "A" << endl;
//
//        if (python_message == "quit"){
//            quit = true;
//        }
//        else if (python_message == "first"){
//            cout << "First Hello!" << endl;
//        }
//        else if (python_message == "second"){
//            cout << "Second Hello!" << endl;
//        }
//        else if (python_message == "third"){
//            cout << "Third Hello!" << endl;
//        }
//        else {
//            cout << "Huh?" << endl;
//        }
//    }
//    return 0;
//}
#include <stdio.h>

int main (int argc, char **argv) {
    for (;;) {
        char buf;
        fread(&buf, 1, 1, stdin);
        if ('q' == buf)
            break;
        fwrite(&buf, 1, 1, stdout);
        fflush(stdout);
    }

    return 0;
}