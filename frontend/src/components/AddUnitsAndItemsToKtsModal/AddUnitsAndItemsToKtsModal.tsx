import React, { useState } from 'react';
import { Modal, Input, Tabs } from 'antd';
import type { IAddUnitsAndItemsToKts } from '../../types/types';
import {
    useAddUnitsAndItemsToKtsMutation,
    useGetCatalogItemsQuery,
    useGetCatalogUnitsQuery,
} from '../../redux/services/catalogApi';
import CatalogItemCard from '../CatalogItemCard/CatalogItemCard';
import CatalogUnitCard from '../CatalogUnitCard/CatalogUnitCard';
import Loader from '../Loader/Loader';

interface AddUnitModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
    ktsId: number;
}

type ITab = 'items' | 'units';

const AddUnitsAndItemsToKtsModal: React.FC<AddUnitModalProps> = ({
    isModalOpen,
    onCancel,
    ktsId,
}) => {
    const [selectedItems, setSelectedItems] = useState<{ item_id: number; quantity: number }[]>([]);
    const [selectedUnits, setSelectedUnits] = useState<{ unit_id: number; quantity: number }[]>([]);
    const [activeTab, setActiveTab] = useState<ITab>('items');

    const { data: items, isError: isItemsError, isLoading: isItemsLoading } = useGetCatalogItemsQuery();
    const { data: units, isError: isUnitsError, isLoading: isUnitsLoading } = useGetCatalogUnitsQuery();
    const [addUnitsAndItems] = useAddUnitsAndItemsToKtsMutation();

    const handleOk = async () => {
        if (selectedItems.length === 0 && selectedUnits.length === 0) {
            alert('Выберите хотя бы один Item или Unit');
            return;
        }

        try {
            const postData: IAddUnitsAndItemsToKts = {
                kts_id: ktsId,
                items: selectedItems.map(({ item_id, quantity }) => ({ item_id, quantity })),
                units: selectedUnits.map(({ unit_id, quantity }) => ({ unit_id, quantity })),
            };
            await addUnitsAndItems(postData)
            setSelectedItems([]);
            setSelectedUnits([]);
            onCancel();
        } catch (error) {
            console.error('Ошибка при добавлении:', error);
        }
    };

    const toggleSelection = (id: number, type: ITab) => {
        if (type === 'items') {
            const exists = selectedItems.some((el) => el.item_id === id);
            const updated = exists
                ? selectedItems.filter((el) => el.item_id !== id)
                : [...selectedItems, { item_id: id, quantity: 1 }];
            setSelectedItems(updated);
        } else {
            const exists = selectedUnits.some((el) => el.unit_id === id);
            const updated = exists
                ? selectedUnits.filter((el) => el.unit_id !== id)
                : [...selectedUnits, { unit_id: id, quantity: 1 }];
            setSelectedUnits(updated);
        }
    };

    const changeQuantity = (id: number, quantity: number, type: ITab) => {
        if (quantity < 1) return;

        if (type === 'items') {
            setSelectedItems(
                selectedItems.map((el) =>
                    el.item_id === id ? { ...el, quantity } : el
                )
            );
        } else {
            setSelectedUnits(
                selectedUnits.map((el) =>
                    el.unit_id === id ? { ...el, quantity } : el
                )
            );
        }
    };

    const renderSelectableList = <T extends { id: number }>(
        data: T[] | undefined,
        selectedList: { item_id?: number; unit_id?: number; quantity: number }[],
        type: ITab,
        renderCard: (item: T) => React.ReactNode,
        selectedColor: string
    ) => {
        return data?.map((item) => {
            const key = type === 'items' ? 'item_id' : 'unit_id';
            const isSelected = selectedList.some((el) => el[key] === item.id);
            const quantity = selectedList.find((el) => el[key] === item.id)?.quantity || 1;

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
        onCancel();
    };

    const isLoading = isItemsLoading || isUnitsLoading;
    const isError = isItemsError || isUnitsError;

    return (
        <Modal
            title="Добавить Items и Units в KTS"
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
                ]}
            />

            {isLoading || isError ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {activeTab === 'items'
                        ? renderSelectableList(
                            items,
                            selectedItems,
                            'items',
                            (item) => <CatalogItemCard item={item} />,
                            '#1890ff'
                        )
                        : renderSelectableList(
                            units,
                            selectedUnits,
                            'units',
                            (unit) => <CatalogUnitCard unit={unit} />,
                            '#52c41a'
                        )}
                </div>
            )}
        </Modal>
    );
};

export default AddUnitsAndItemsToKtsModal;
