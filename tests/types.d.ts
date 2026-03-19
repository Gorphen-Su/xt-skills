// 测试类型定义
declare namespace jest {
  interface DoneCallback {
    (err?: Error): void;
  }

  interface ExpectStatic {
    /**
     * 断言值为真
     */
    toBetruthy(): void;
    /**
     * 断言值为假
     */
    toBeFalsy(): void;
    /**
     * 断言值包含子字符串
     */
    toContain(target: string): void;
    /**
     * 断言值匹配正则表达式
     */
    toMatch(pattern: RegExp): void;
  }

  interface Matchers<R> {
    /**
     * 断言函数抛出错误
     */
    toThrow(error?: Error | string | RegExp): void;
    /**
     * 断言值为真
     */
    toBeTruthy(): void;
    /**
     * 断言值为假
     */
    toBeFalsy(): void;
    /**
     * 断言值包含子字符串
     */
    toContain(target: string): void;
    /**
     * 断言值匹配正则表达式
     */
    toMatch(pattern: RegExp): void;
    /**
     * 断言值等于预期值
     */
    toEqual(expected: unknown): void;
  }
}

// Fixture 创建函数类型定义
type UserFixture = {
  id: string;
  name: string;
  email: string;
  createdAt: Date;
};

type OrderFixture = {
  id: string;
  userId: string;
  total: number;
  status: 'pending' | 'completed' | 'cancelled';
  createdAt: Date;
};

declare namespace fixtures {
  function createUserFixture(overrides?: Partial<UserFixture>): UserFixture;
  function createOrderFixture(overrides?: Partial<OrderFixture>): OrderFixture;
}
