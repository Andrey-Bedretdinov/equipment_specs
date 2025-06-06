import { Button, Card, Typography } from "antd";
import { DownOutlined, RightOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { IKts } from "../../types/types";
import UnitCardsList from "../UnitCardsList/UnitCardsList";
import ItemCardsList from "../ItemCardsList/ItemCardsList";
import { useState } from "react";
import { useLocation } from "react-router-dom";

import styles from './KtsCard.module.css';
import AddUnitsAndItemsToKtsModal from "../AddUnitsAndItemsToKtsModal/AddUnitsAndItemsToKtsModal";

const { Text, Title } = Typography;

interface KtsCardProps {
    kts: IKts;
}
const KtsCard: React.FC<KtsCardProps> = ({ kts }) => {

    const [collapsed, setCollapsed] = useState<boolean>(true);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);

    const toggleCollapse = () => {
        setCollapsed(prev => !prev);
    };

    const location = useLocation();
    const isProject = location.pathname.startsWith('/project');
    const isCatalogKtsPage = location.pathname.startsWith('/catalog/kts');

    return (
        <Card
            title={
                <div className={styles.cardTitle}>
                    <Button
                        type="text"
                        icon={collapsed ? <RightOutlined /> : <DownOutlined />}
                        onClick={toggleCollapse}
                    />
                    <div className={styles.cardDesc}>
                        <div>
                            <Title level={2}>{kts.name}</Title>
                            <Text>{kts.description}</Text><br />
                            <Text strong>Итоговая стоимость: {kts.price} RUB</Text>
                        </div>
                        <div className={styles.btnBox}>
                            {isCatalogKtsPage && (
                                <Button
                                    type="primary"
                                    icon={<EditOutlined />}
                                    onClick={() => setIsModalOpen(true)}
                                />
                            )}

                            <Button
                                type="primary"
                                danger
                                icon={<DeleteOutlined />}
                                // onClick={handleDelete}
                            />
                        </div>
                    </div>
                </div>
            }
            className={styles.card}
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
            {isModalOpen &&
                <AddUnitsAndItemsToKtsModal
                    isModalOpen={isModalOpen}
                    onCancel={() => setIsModalOpen(false)}
                    ktsId={kts.id}
                />
            }
        </Card>
    );
};

export default KtsCard;