/** @type {import('jest').Config} */
module.exports = {
  testEnvironment: 'node',
  transform: {
    '^.+\\.ts$': ['ts-jest', { useESM: false }],
  },
  testMatch: ['**/tests/**/*.test.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
  ],
  modulePathIgnorePatterns: [
    '<rootDir>/tests/fixtures/',
    '<rootDir>/node_modules/',
    '<rootDir>/dist/',
  ],
};
