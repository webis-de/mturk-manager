import type { ID } from '@/modules/app/types';

export interface EntityInterface {
  id?: ID;
  // [key: string]: any;
}

// export interface ServiceEntityInterface<T> {
//   useCreate(
//     ...args: unknown[]
//   ): {
//     entity: Ref<T>;
//     create(...args: unknown[]): Promise<T>;
//   };
//   create(entity: T): Promise<T>;
//
//   useUpdate(
//     entityPassed: T,
//   ): {
//     entity: Ref<T>;
//     update(): Promise<void>;
//   };
//   update(entity: T): Promise<T>;
//
//   useDelete(): {
//     delete(entity: T): Promise<boolean>;
//   };
//   delete(entity: T): Promise<boolean>;
// }
