export type ID = number | string;

export type Optional<T, K extends keyof T> = Pick<T, K> & Partial<T>;

export type BaseDialogParamsSubmit = {
  close: () => void;
};
