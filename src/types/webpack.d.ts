// src/types/webpack.d.ts
declare const require: {
  context(
    directory: string,
    useSubdirectories: boolean,
    regExp: RegExp
  ): {
    keys(): string[];
    <T = any>(id: string): T;
  };
};
