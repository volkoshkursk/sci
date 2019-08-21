#include <cstring>
#include <iostream>
#include <math.h> 

using namespace std;

#ifdef __cplusplus
extern "C" double mi(char** news, unsigned n2, char* class_, char** classes, char* word)
#else
double mi(char** news, unsigned n2, char* class_, char** classes, char* word)
#endif
{
	long double N11 = 0;
	long double N10 = 0;
	long double N01 = 0;
	long double N00 = 0;
	for(unsigned j = 0; j < n2; j++)
	{
		if(strstr(classes[j], class_) != NULL)
		{
//			cout << "class+" << endl;
			if(strstr(news[j], word) != NULL) 
			{
//				cout << "word+" << endl;
				N11 ++;
			}
			else 
			{
//				cout << "word-" << endl;
				N01 ++;
			}
		}
		else 
		{
//			cout << "class-" << endl;
			if(strstr(news[j], word) != NULL) 
			{
//				cout << "word+" << endl;
				N10 ++;
			}
			else 
			{
//				cout << "word-" << endl;
				N00 ++;
			}
		}
//		cout<< "N11 " << N11<<endl;
//		cout<< "N10 " << N10<<endl;
//		cout<< "N01 " << N01<<endl;
//		cout<< "N00 " << N00<<endl;
	}
	if((N11*N10*N00*N01) != 0)
	{
		long double N = N11+N10+N00+N01;
		long double N1x = N11+N10;
		long double Nx1 = N11 + N01;
		long double N0x = N01+N00;
		long double Nx0 = N10 + N00;
//		cout<< "N " << N<<endl;
//		cout<< "N1x " << N1x<<endl;
//		cout<< "Nx1 " << Nx1<<endl;
//		cout<< "N0x " << N0x<<endl;
//		cout<< "Nx0 " << Nx0<<endl;
//		cout << (N11/N) * log2((N*N11)/(N1x*Nx1)) << endl;
//		cout << (N01/N) * log2((N*N01)/(N0x*Nx1))<< endl;
//		cout << (N10/N) * log2((N*N10)/(N1x*Nx0)) << endl;
//		cout << (N00/N) * log2((N*N00)/(N0x*Nx0)) << endl;
//		cout << (((N11/N)*log2((N*N11)/(N1x*Nx1))) + ((N01/N) * log2((N*N01)/(N0x*Nx1))) + ((N10/N) * log2((N*N10)/(N1x*Nx0))) + ((N00/N) * log2((N*N00)/(N0x*Nx0))))<< endl << endl;
		return (((N11/N)*log2((N*N11)/(N1x*Nx1))) + ((N01/N) * log2((N*N01)/(N0x*Nx1))) + ((N10/N) * log2((N*N10)/(N1x*Nx0))) + ((N00/N) * log2((N*N00)/(N0x*Nx0))));
	}
	else
	{
		return -1;
	}
//		PyList_Append(out, PyInt_FromLong(i));
}

//int main()
//{
//	
//	return 1;
//}
#ifdef __cplusplus
extern "C" int count(char** arr, unsigned n2, char* word)
#else
int count(char** arr, unsigned n2, char* word)
#endif
{
	int out = 0;
	for(unsigned j = 0; j < n2; j++)
	{
		if(strstr(arr[j], word) != NULL) {out ++;}
	}
	return out;
}