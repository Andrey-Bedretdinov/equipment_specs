import type { DataNode } from "antd/es/tree"
import type { SpecNode } from "../types/types"

// ——— Функция преобразования ———
export function transformToTreeData(nodes: SpecNode[]): DataNode[] {
    return nodes.map((node) => {
        let title: React.ReactNode = node.title

        if (node.type === 'item') {
            title = (
                <div>
                    <div>{node.productName} </div>
                    <small>
                        {node.manufacturer}, {node.supplierName}, {node.quantity} шт × {node.price} {node.currency}
                    </small>
                </div>
            )
        }

        return {
            key: node.key,
            title,
            children: node.children ? transformToTreeData(node.children) : undefined,
        }
    })
}