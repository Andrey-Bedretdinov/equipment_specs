interface INode {
  id: number;
  name: string;
  description: string;
  price: string;
}

export interface IItem extends INode {
  supplier: string;
  catalog_code: string;
  currency: string;
  manufactured: string;
  delivery_type: string;
  quantity: number;
}

export interface IUnit extends INode {
  items_list?: IItem[];
  quantity: number;
}

export interface IKts extends INode {
  units_list?: IUnit[];
  items_list?: IItem[];
  quantity: number;
}

export interface IProject extends INode {
  kts_list?: IKts[];
  units_list?: IUnit[];
  items_list?: IItem[];
}