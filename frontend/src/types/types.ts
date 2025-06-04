export type SpecNodeType = 'project' | 'ktc' | 'unit' | 'item'

export interface BaseNode {
  id: number;
  name: string;
  description: string;
}

export interface ItemNode extends BaseNode {
  supplier: string
  catalog_code: string
  price: number
  currency: string
  manufacturer: string
  deliveryType: string
  quantity: number
}

export interface UnitNode extends BaseNode {
  items: ItemNode[]
  quantity: number;
}

export interface KtcNode extends BaseNode {
  untis: UnitNode[]
  quantity: number;
}

export interface ProjectNode extends BaseNode {
  kts: KtcNode[]
}

export type SpecNode = ProjectNode | KtcNode | UnitNode | ItemNode


// ТИПЫ ДЛЯ ПОДХОДА С КАРТОЧКАМИ

export interface IProject {
  id: number;
  name: string;
  description: string;
}

export interface IProjectKtsLink {
  id: number;
  project: number;
  catalog_kts: number;
}