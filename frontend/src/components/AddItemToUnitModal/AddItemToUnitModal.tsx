import React, { useState } from 'react';
import { Modal, Input } from 'antd';
import type { IAddItemToUnit } from '../../types/types';
import {
    useAddCatalogItemsToUnitMutation,
    useGetCatalogItemsQuery,
} from '../../redux/services/catalogApi';
import CatalogItemCard from '../CatalogItemCard/CatalogItemCard';
import Loader from '../Loader/Loader';

interface AddUnitModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
    unitId: number;
}

const AddItemToUnitModal: React.FC<AddUnitModalProps> = ({ isModalOpen, onCancel, unitId }) => {
    const [selectedItems, setSelectedItems] = useState<{ id: number; quantity: number }[]>([]);

    const { data: items, isError, isLoading } = useGetCatalogItemsQuery();
    const [addItemsToUnit] = useAddCatalogItemsToUnitMutation();

    const handleOk = async () => {
        if (selectedItems.length === 0) {
            alert('Выберите хотябы один Item');
            return ;
        }

        try {
            const postData: IAddItemToUnit = { id: unitId, items: selectedItems };
            await addItemsToUnit(postData).unwrap();
            setSelectedItems([]);
            onCancel();
        } catch (error) {
            console.error('Ошибка при добавлении:', error);
        }
    };

    const toggleItem = (itemId: number) => {
        setSelectedItems((prev) => {
            const exists = prev.find((el) => el.id === itemId);
            return exists
                ? prev.filter((el) => el.id !== itemId)
                : [...prev, { id: itemId, quantity: 1 }];
        });
    };

    const updateQuantity = (itemId: number, quantity: number) => {
        if (quantity < 1) return;
        setSelectedItems((prev) =>
            prev.map((el) => (el.id === itemId ? { ...el, quantity } : el))
        );
    };

    const handleCancel = () => {
        setSelectedItems([]);
        onCancel();
    };

    return (
        <Modal
            title="Добавить Items в Unit"
            open={isModalOpen}
            onCancel={handleCancel}
            onOk={handleOk}
            okText="Сохранить"
            cancelText="Отмена"
            styles={{ body: { maxHeight: '60vh', overflowY: 'auto' } }}
        >
            {isLoading || isError ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {items?.map((item) => {
                        const isSelected = selectedItems.some((el) => el.id === item.id);
                        const quantity = selectedItems.find((el) => el.id === item.id)?.quantity || 1;

                        return (
                            <div
                                key={item.id}
                                onClick={() => toggleItem(item.id)}
                                style={{
                                    border: isSelected ? '2px solid #1890ff' : '',
                                    borderRadius: 8,
                                    padding: 6,
                                    cursor: 'pointer',
                                }}
                            >
                                <CatalogItemCard item={item} />
                                {isSelected && (
                                    <Input
                                        type="number"
                                        min={1}
                                        value={quantity}
                                        onChange={(e) =>
                                            updateQuantity(item.id, Number(e.target.value))
                                        }
                                        onClick={(e) => e.stopPropagation()}
                                        style={{ width: 80, marginTop: 8 }}
                                        placeholder="Количество"
                                    />
                                )}
                            </div>
                        );
                    })}
                </div>
            )}
        </Modal>
    );
};

export default AddItemToUnitModal;
