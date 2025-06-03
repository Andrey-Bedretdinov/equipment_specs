import { useState } from "react";
import { Card, Space, Typography, Button } from 'antd';
import { DownOutlined, RightOutlined } from '@ant-design/icons';

import type { UnitNode } from "../../types/types";
import ItemCard from "../ItemCard/ItemCard";
import styles from './UnitBlock.module.css';

const { Title, Text } = Typography;

const UnitBlock: React.FC<{ unit: UnitNode }> = ({ unit }) => {
    const [expanded, setExpanded] = useState(false);

    return (
        <Card
            className={styles.card}
            title={
                <div className={styles.titleRow}>
                    <Button
                        type="text"
                        icon={expanded ? <DownOutlined /> : <RightOutlined />}
                        onClick={() => setExpanded(!expanded)}
                    />
                    <Text strong>{unit.name}</Text>
                </div>
            }
        >
            <Text>{unit.description}</Text>

            {expanded && (
                <div className={styles.children}>
                    <Title level={5}>Items:</Title>
                    <Space direction="vertical" className={styles.children}>
                        {unit.items.map((item) => <ItemCard key={item.id} item={item} />)}
                    </Space>
                </div>
            )}
        </Card>
    );
};

export default UnitBlock;
