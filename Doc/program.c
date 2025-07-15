void push (int value, Stack *stp) {
  if (stp->top == stp->size) {
    doubleStackSize(stp);
  }
  stp->array[stp->top] = value;
  stp->top++;
}
