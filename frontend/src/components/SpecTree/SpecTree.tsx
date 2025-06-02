import { Tree } from 'antd'
import React from 'react'
import { transformToTreeData } from '../../utils/treeDataTransfrom'
import { treeData } from '../../constants/treeData'

const SpecTree: React.FC = () => {
    const treeNodes = transformToTreeData(treeData)

    return (
        <div>
            <h2>Структура спецификации</h2>
            <Tree
                showLine
                defaultExpandAll
                treeData={treeNodes}
            />
        </div>
    )
}

export default SpecTree;
