#include <stdio.h>
#include <stdlib.h>

// Heap Sort
void recursive_branch_swap(int *lst, int size);
void recursive_heapify(int *lst, int size);
void recursive_extract(int *lst, int size);

int main() {
    // Example usage
    int a_list[] = {1, 166, 133, 5, 6, 7};
    int size = sizeof(a_list) / sizeof(a_list[0]);
    recursive_extract(a_list,6);

    
  
    // Print heap-sorted array
    printf("\nHeap-sorted array: ");
    for (int i = 0; i < size; i++) {
        printf("%d ", a_list[i]);
    }


    return 0;
}



void recursive_branch_swap(int *lst, int size) {
    if (size <= 1) {
        return;
    }
    int node = size / 2 - 1;
    if (lst[size - 1] > lst[node]) {
        int temp = lst[size - 1];
        lst[size - 1] = lst[node];
        lst[node] = temp;
    }
    recursive_branch_swap(lst, size / 2);
}

void recursive_heapify(int *lst, int size) {
    if (size <= 1) {
        return;
    }
    recursive_branch_swap(lst, size);
    recursive_heapify(lst, size - 1);
}


void recursive_extract(int *lst, int size) {
    if (size <= 1) {
        return;
    }
    recursive_heapify(lst, size);
    int temp = lst[size - 1];
    lst[size - 1] = lst[0];
    lst[0] = temp;
    recursive_extract(lst, size - 1);
}
