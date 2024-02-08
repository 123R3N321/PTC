#include <stdio.h>

void iterative_heapify(int lst[], int size) {
    int begin = size - 1;
    while (begin >= 0) {
        int branch_end = begin;
        while (branch_end != 0) {
            int prev = branch_end / 2;
            if (lst[branch_end] > lst[prev]) {
                int temp = lst[branch_end];
                lst[branch_end] = lst[prev];
                lst[prev] = temp;
            }
            branch_end /= 2;
        }
        begin -= 1;
    }
}

void iterative_extract(int lst[], int length) {
    int begin = length - 1;
    while (begin >= 0) {
        iterative_heapify(lst, begin + 1);
        int temp = lst[begin];
        lst[begin] = lst[0];
        lst[0] = temp;
        begin -= 1;
    }
}

int main() {
    int lst[] = {1, 9, 2, 4, 8, 7, 3, 5, 6};
    int length = sizeof(lst) / sizeof(lst[0]);
    iterative_extract(lst, length);
    printf("Sorted array:\n");
    for (int i = 0; i < length; ++i) {
        printf("%d ", lst[i]);
    }
    printf("\n");
    return 0;
}
