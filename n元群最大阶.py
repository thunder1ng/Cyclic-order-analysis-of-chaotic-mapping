from math import gcd

class Solution:
    def integerBreakForLCM(self, n: int) -> int:
        # DP数组建立，注意数组本身容量赋值
        dp = [1] * (n + 1)
        # 初始化
        dp[2] = 1
        
        for i in range(3, n + 1):
            # 记录dp[i]最大值
            result = 0
            for j in range(1, i):
                # 计算拆分的两种情况，并取最大值
                lcm1 = abs(j * (i - j)) // gcd(j, (i - j))
                lcm2 = abs(j * dp[i - j]) // gcd(j, dp[i - j])
                result = max(result, max(lcm1, lcm2))
            # 最大值存在dp[i]里
            dp[i] = result
        
        return dp[n]

# 测试例子
solution = Solution()
max_orders =  []
for i in range(10,60):
    max_orders.append(solution.integerBreakForLCM(i))
print(max_orders)
