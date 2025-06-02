export type SpecNodeType = 'project' | 'ktc' | 'unit' | 'item'

export interface BaseNode {
  id: number                // ID из базы, используется в API
  key: string               // ключ для дерева (строка, уникальный в UI)
  title: string             // заголовок для отображения
  type: SpecNodeType        // тип узла
  children?: SpecNode[]     // вложенные элементы
}

export interface ItemNode extends BaseNode {
  type: 'item'
  supplierName: string
  catalogCode: string
  productName: string
  quantity: number
  price: number
  manufacturer: string
  currency: string
  deliveryType: string
}

export interface UnitNode extends BaseNode {
  type: 'unit'
  children: ItemNode[]
}

export interface KtcNode extends BaseNode {
  type: 'ktc'
  children: UnitNode[]
}

export interface ProjectNode extends BaseNode {
  type: 'project'
  children: KtcNode[]
}

export type SpecNode = ProjectNode | KtcNode | UnitNode | ItemNode
