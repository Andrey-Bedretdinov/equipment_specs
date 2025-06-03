import { useState } from "react";
import { Button, Card, Space, Typography } from 'antd';
import { DownOutlined, RightOutlined } from '@ant-design/icons';

import type { KtcNode } from "../../types/types";
import UnitBlock from "../UnitBlock/UnitBlock";
import styles from './KtsBlock.module.css';

const { Title, Text } = Typography;

const KtcBlock: React.FC<{ ktc: KtcNode }> = ({ ktc }) => {
    const [expanded, setExpanded] = useState<boolean>(false);

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
                    <Text strong>{ktc.name}</Text>
                </div>
            }
        >
            <Text>{ktc.description}</Text>

            {expanded && (
                <div className={styles.children}>
                    <Title level={4}>Units:</Title>
                    <Space direction="vertical" className={styles.children}>
                        {ktc.untis.map((unit) => (
                            <UnitBlock key={unit.id} unit={unit} />
                        ))}
                    </Space>
                </div>
            )}
        </Card>
    );
};

export default KtcBlock;
