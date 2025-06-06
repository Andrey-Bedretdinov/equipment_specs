import { Button, Card, Typography } from "antd";
import { DownOutlined, RightOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { IKts } from "../../types/types";
import UnitCardsList from "../UnitCardsList/UnitCardsList";
import ItemCardsList from "../ItemCardsList/ItemCardsList";
import { useState } from "react";
import { useLocation, useParams } from "react-router-dom";

import styles from './KtsCard.module.css';
import AddUnitsAndItemsToKtsModal from "../AddUnitsAndItemsToKtsModal/AddUnitsAndItemsToKtsModal";
import { useDeleteKtsMutation } from "../../redux/services/catalogApi";
import { useDeleteElementsFromProjectMutation } from "../../redux/services/projectsApi";

const { Text, Title } = Typography;

interface KtsCardProps {
    kts: IKts;
}
const KtsCard: React.FC<KtsCardProps> = ({ kts }) => {

    const [collapsed, setCollapsed] = useState<boolean>(true);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const { project_id } = useParams();

    const [deleteItemFromProject] = useDeleteElementsFromProjectMutation();

    const [deleteKts] = useDeleteKtsMutation();

    const toggleCollapse = () => {
        setCollapsed(prev => !prev);
    };

    const handleDelete = () => {
        if (isCatalogKtsPage) deleteKts(kts.id)
        else if (isProject && project_id) {
            deleteItemFromProject({ project_id: project_id, kts: [{ kts_id: kts.id }] })
        }
    }

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
                                onClick={handleDelete}
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