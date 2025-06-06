import { Button, Card, Typography } from "antd";
import { DownOutlined, RightOutlined } from '@ant-design/icons';
import type { IKts } from "../../types/types";
import UnitCardsList from "../UnitCardsList/UnitCardsList";
import ItemCardsList from "../ItemCardsList/ItemCardsList";
import { useState } from "react";
import { useLocation } from "react-router-dom";
const { Text, Title } = Typography;

interface KtsCardProps {
    kts: IKts;
}
const KtsCard: React.FC<KtsCardProps> = ({ kts }) => {

    const [collapsed, setCollapsed] = useState<boolean>(true);

    const toggleCollapse = () => {
        setCollapsed(prev => !prev);
    };

    const location = useLocation();
    const isProject = location.pathname.startsWith('/project');

    return (
        <Card
            title={
                <div
                    style={{ display: 'flex', alignItems: 'center', gap: 16 }}
                >
                    <Button
                        type="text"
                        icon={collapsed ? <RightOutlined /> : <DownOutlined />}
                        onClick={toggleCollapse}
                    />
                    <div>
                        <Title level={2}>{kts.name}</Title>
                        <Text>{kts.description}</Text><br />
                        <Text strong>Итоговая стоимость: {kts.price} RUB</Text>
                    </div>
                </div>
            }
            style={{
                width: '100%',
                marginBottom: 16,
                backgroundColor: '#fafafa',
                borderLeft: '4px solid #faad14',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            }}
        >
            {!collapsed && (
                <>
                    <UnitCardsList
                        canDelete={!isProject}
                        units_list={kts.units_list ?? []}
                    />
                    <ItemCardsList
                        canDelete={!isProject}
                        items_list={kts.items_list ?? []}
                    />
                </>
            )}
        </Card>
    );
};

export default KtsCard;