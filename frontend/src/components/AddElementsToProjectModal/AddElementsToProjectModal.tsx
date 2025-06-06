import React, { useState } from 'react';
import { Modal, Input, Tabs } from 'antd';
import type { IAddElementsToProjects } from '../../types/types';
import {
    useGetCatalogItemsQuery,
    useGetCatalogUnitsQuery,
    useGetCatalogKtsQuery,
} from '../../redux/services/catalogApi';
import CatalogItemCard from '../CatalogItemCard/CatalogItemCard';
import CatalogUnitCard from '../CatalogUnitCard/CatalogUnitCard';
import CatalogKtsCard from '../CatalogKtsCard/CatalogKtsCard';
import Loader from '../Loader/Loader';

interface AddElementsModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
    projectId: number;
}

type ITab = 'items' | 'units' | 'kts';

const AddElementsToProjectModal: React.FC<AddElementsModalProps> = ({
    isModalOpen,
    onCancel,
    projectId,
}) => {
    const [selectedItems, setSelectedItems] = useState<{ id: number; quantity: number }[]>([]);
    const [selectedUnits, setSelectedUnits] = useState<{ id: number; quantity: number }[]>([]);
    const [selectedKts, setSelectedKts] = useState<{ id: number; quantity: number }[]>([]);
    const [activeTab, setActiveTab] = useState<ITab>('items');

    const { data: items, isError: isItemsError, isLoading: isItemsLoading } = useGetCatalogItemsQuery();
    const { data: units, isError: isUnitsError, isLoading: isUnitsLoading } = useGetCatalogUnitsQuery();
    const { data: kts, isError: isKtsError, isLoading: isKtsLoading } = useGetCatalogKtsQuery();

    const handleOk = async () => {
        if (selectedItems.length === 0 && selectedUnits.length === 0 && selectedKts.length === 0) {
            alert('Выберите хотя бы один Item, Unit или KTS');
            return;
        }

        try {
            const postData: IAddElementsToProjects = {
                id: projectId,
                items: selectedItems,
                units: selectedUnits,
                kts: selectedKts,
            };
            console.log(postData);
            setSelectedItems([]);
            setSelectedUnits([]);
            setSelectedKts([]);
            onCancel();
        } catch (error) {
            console.error('Ошибка при добавлении:', error);
        }
    };

    const toggleSelection = (id: number, type: ITab) => {
        const [setFunc, list] = (() => {
            switch (type) {
                case 'items': return [setSelectedItems, selectedItems] as const;
                case 'units': return [setSelectedUnits, selectedUnits] as const;
                case 'kts': return [setSelectedKts, selectedKts] as const;
            }
        })();

        const updated = list.some((el) => el.id === id)
            ? list.filter((el) => el.id !== id)
            : [...list, { id, quantity: 1 }];

        setFunc(updated);
    };

    const changeQuantity = (id: number, quantity: number, type: ITab) => {
        if (quantity < 1) return;
        const [setFunc, list] = (() => {
            switch (type) {
                case 'items': return [setSelectedItems, selectedItems] as const;
                case 'units': return [setSelectedUnits, selectedUnits] as const;
                case 'kts': return [setSelectedKts, selectedKts] as const;
            }
        })();

        setFunc(list.map((el) => (el.id === id ? { ...el, quantity } : el)));
    };

    const renderSelectableList = <T extends { id: number }>(
        data: T[] | undefined,
        selectedList: { id: number; quantity: number }[],
        type: ITab,
        renderCard: (item: T) => React.ReactNode,
        selectedColor: string
    ) => {
        return data?.map((item) => {
            const isSelected = selectedList.some((el) => el.id === item.id);
            const quantity = selectedList.find((el) => el.id === item.id)?.quantity || 1;

            return (
                <div
                    key={item.id}
                    onClick={() => toggleSelection(item.id, type)}
                    style={{
                        border: isSelected ? `2px solid ${selectedColor}` : '',
                        borderRadius: 8,
                        padding: 6,
                        cursor: 'pointer',
                    }}
                >
                    {renderCard(item)}
                    {isSelected && (
                        <Input
                            type="number"
                            min={1}
                            value={quantity}
                            onChange={(e) => changeQuantity(item.id, Number(e.target.value), type)}
                            onClick={(e) => e.stopPropagation()}
                            style={{ width: 80, marginTop: 8 }}
                            placeholder="Количество"
                        />
                    )}
                </div>
            );
        });
    };

    const handleCancel = () => {
        setSelectedItems([]);
        setSelectedUnits([]);
        setSelectedKts([]);
        onCancel();
    };

    const isLoading = isItemsLoading || isUnitsLoading || isKtsLoading;
    const isError = isItemsError || isUnitsError || isKtsError;

    return (
        <Modal
            title="Добавить элементы в KTS"
            open={isModalOpen}
            onCancel={handleCancel}
            onOk={handleOk}
            okText="Сохранить"
            cancelText="Отмена"
            styles={{ body: { height: '60vh', overflowY: 'auto' } }}
        >
            <Tabs
                activeKey={activeTab}
                onChange={(key) => setActiveTab(key as ITab)}
                items={[
                    { key: 'items', label: 'Items' },
                    { key: 'units', label: 'Units' },
                    { key: 'kts', label: 'KTS' },
                ]}
            />

            {isLoading || isError ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {activeTab === 'items' &&
                        renderSelectableList(
                            items,
                            selectedItems,
                            'items',
                            (item) => <CatalogItemCard item={item} />,
                            '#1890ff'
                        )}
                    {activeTab === 'units' &&
                        renderSelectableList(
                            units,
                            selectedUnits,
                            'units',
                            (unit) => <CatalogUnitCard unit={unit} />,
                            '#52c41a'
                        )}
                    {activeTab === 'kts' &&
                        renderSelectableList(
                            kts,
                            selectedKts,
                            'kts',
                            (kt) => <CatalogKtsCard kts={kt} />,
                            '#faad14'
                        )}
                </div>
            )}
        </Modal>
    );
};

export default AddElementsToProjectModal;
