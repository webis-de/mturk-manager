import { EntityInterface } from '@/modules/app/entity/entity.types';
import { ID } from '@/modules/app/types';

export class Entity implements EntityInterface {
  id?: ID;

  protected constructor(data: EntityInterface) {
    this.id = data.id;
  }

  static async convertFromServerToStore<T extends Entity>(
    data: EntityInterface[],
  ): Promise<{ [key: string]: T }> {
    const entities: T[] = await Promise.all(
      data.map((item: EntityInterface) => (this.parseFromServer(item)) as Promise<T>),
    );

    return entities.reduce((acc, entity) => {
      acc[entity.id as ID] = entity;
      return acc;
    }, {} as { [key: string]: T });
  }

  static async parseFromServer(data: EntityInterface): Promise<Entity> {
    return new this(data);
  }

  prepareForServer(): { [key: string]: unknown } {
    return { id: this.id };
  }
}
