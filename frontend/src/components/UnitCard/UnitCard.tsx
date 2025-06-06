import { Button, Card, Typography } from "antd";
import { DownOutlined, RightOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import type { IUnit } from "../../types/types";
import ItemCardsList from "../ItemCardsList/ItemCardsList";
import { useState } from "react";

import styles from './UnitCard.module.css';
import { useLocation, useParams } from "react-router-dom";
import AddItemToUnitModal from "../AddItemToUnitModal/AddItemToUnitModal";
import { useDeleteUnitMutation } from "../../redux/services/catalogApi";
import { useDeleteElementsFromProjectMutation } from "../../redux/services/projectsApi";
const { Text, Title } = Typography;

interface UnitCardProps {
    unit: IUnit;
    canDelete?: boolean;
}

const UnitCard: React.FC<UnitCardProps> = ({ unit, canDelete = true }) => {

    const [collapsed, setCollapsed] = useState<boolean>(true);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
    const { project_id } = useParams();

    const [deleteUnit] = useDeleteUnitMutation();
    const [deleteItemFromProject] = useDeleteElementsFromProjectMutation();

    const location = useLocation();
    const isProject = location.pathname.startsWith('/project');
    const isCatalogUnitsPage = location.pathname.startsWith('/catalog/units');
    const isCatalogKtsPage = location.pathname.startsWith('/catalog/kts');

    const toggleCollapse = () => {
        setCollapsed(prev => !prev);
    };

    const handleDelete = () => {
        if (isCatalogUnitsPage) {
            deleteUnit(unit.id);
        } else if (isCatalogKtsPage) {
            console.log('Уделение Юнита из каталога ктс')
        } else if (isProject && project_id) {
            deleteItemFromProject({ project_id: project_id, units: [{ unit_id: unit.id }] })
        }
    }

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
                            <Title level={3}>{unit.name}</Title>
                            <Text>{unit.name}</Text><br />
                            <Text strong>Итоговая стоимость: {unit.price} RUB</Text>
                        </div>


                        <div className={styles.btnBox}>
                            {isCatalogUnitsPage && (
                                <Button
                                    type="primary"
                                    icon={<EditOutlined />}
                                    onClick={() => setIsModalOpen(true)}
                                />
                            )}

                            {canDelete && (
                                <Button
                                    type="primary"
                                    danger
                                    icon={<DeleteOutlined />}
                                    onClick={handleDelete}
                                />
                            )}
                        </div>
                    </div>
                </div>
            }
            className={styles.card}
        >
            {!collapsed &&
                <ItemCardsList
                    canDelete={isCatalogKtsPage || isProject ? false : true}
                    items_list={unit.items_list ?? []}
                />
            }

            {isModalOpen &&
                <AddItemToUnitModal
                    isModalOpen={isModalOpen}
                    onCancel={() => setIsModalOpen(false)}
                    unitId={unit.id}
                />}
        </Card>
    )

}

export default UnitCard;