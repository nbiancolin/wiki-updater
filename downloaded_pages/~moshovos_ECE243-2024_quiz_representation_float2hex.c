// the fist output line is the floating point as represented in binary printed out in hexadecimal
// the second line is the floating point value represented
// this may be different than what you specify in the assignment. Why?

float f = 1.25;

unsigned int *a = & f;

main()
{
  printf ("%x\n", *a);
  printf ("%f\n", f);
}