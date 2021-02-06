# class node(object):
#     def __init__(self, data):
#         self._data = data
#         self._next = None

#     def get_data(self):
#         return self._data

#     def get_next(self):
#         return self._next

#     def set_data(self, data):
#         self._data = data

#     def set_next(self, next):
#         self._next = next


# class Linklist(object):
#     def __init__(self):
#         self.head = None

#     def add(self, data):
#         new_node = node(data)
#         new_node.set_next(self.head)
#         self.head = new_node

#     def search(self, data):
#         checking = self.head
#         while checking != None:
#             if checking.get_data() == data:
#                 break
#             checking = checking.get_next()
#         if checking == None:
#             return 0
#         else:
#             return 1

#     def remove(self, data):
#         left = None
#         right = self.head
#         while right != None:
#             if right.get_data() == data:
#                 break
#             left = right
#             right = right.get_next()
#         if left == None:
#             self.head = None
#         else:
#             left.set_next(right.get_next())

#     def isempty(self):
#         return self.head == None

#     def size(self):
#         sum = 0
#         checking = self.head
#         while checking != None:
#             sum = sum+1
#             checking = checking.get_next()
#         return sum

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None


# class Linklist(object):
#     def __init__(self):
#         self.head = None
#         self.tail = None

#     def add(self, data):
#         new_node = ListNode(data)
#         if self.head == None:
#             new_node.next = self.head
#             self.head = new_node
#             self.tail = new_node
#         else:
#             self.tail.next = new_node
#             self.tail = new_node
#     def size(self):
#         sum = 0
#         checking = self.head
#         while checking != None:
#             sum = sum+1
#             checking = checking.next
#         return sum

# class Solution:
#     def deleteDuplicates(self, head: ListNode) -> ListNode:
#         p = pp = head
#         ans = []
#         if p == None:
#             return ans
#         while pp != None:
#             ans.append(pp.val)
#             while (p.next != None) and (p.val == p.next.val):
#                 p = p.next
#             if p.next == None:
#                 pp.next = None
#                 p = pp = None
#             else:
#                 pp.next = p.next
#                 pp = p.next
#                 p = p.next
#         return ans


# a = Linklist()
# a.add(1)
# a.add(2)
# a.add(2)
# a.add(3)
# print('a的长度', a.size())
# print('尾指针位置初数值',a.tail.val)
# solu = Solution().deleteDuplicates(a.head)
# print(solu)
from typing import List
class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        nums=nums1[0:m]+nums2[0:n]
        nums1[:]=QuickSort().quick_sort(nums)
        
class QuickSort(object):
    def quick_sort(self,L):
        return self.q_sort(L, 0, len(L) - 1)

    def q_sort(self,L, left, right):
        if left < right:
            pivot = self.Partition(L, left, right)

            self.q_sort(L, left, pivot - 1)
            self.q_sort(L, pivot + 1, right)
        return L

    def Partition(self,L, left, right):
        pivotkey = L[left]

        while left < right:
            while left < right and L[right] >= pivotkey:
                right -= 1
            L[left] = L[right]
            while left < right and L[left] <= pivotkey:
                left += 1
            L[right] = L[left]

        L[left] = pivotkey
        return left



