import React, { useState } from 'react';
import { Modal, Input, Tabs } from 'antd';
import type { IAddUnitsAndItemsToKts } from '../../types/types';
import {
    // useAddCatalogItemsToUnitMutation,
    useGetCatalogItemsQuery,
    useGetCatalogUnitsQuery,
} from '../../redux/services/catalogApi';
import CatalogItemCard from '../CatalogItemCard/CatalogItemCard';
import Loader from '../Loader/Loader';
import CatalogUnitCard from '../CatalogUnitCard/CatalogUnitCard';

interface AddUnitModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
    ktsId: number;
}

type ITab = 'items' | 'units'

const AddUnitsAndItemsToKtsModal: React.FC<AddUnitModalProps> = ({
    isModalOpen,
    onCancel, ktsId
}) => {
    const [selectedItems, setSelectedItems] = useState<{ id: number; quantity: number }[]>([]);
    const [selectedUnits, setSelectedUnits] = useState<{ id: number; quantity: number }[]>([]);

    const [activeTab, setActiveTab] = useState<ITab>('items');

    const { data: items, isError, isLoading } = useGetCatalogItemsQuery();
    const { data: units } = useGetCatalogUnitsQuery();

    // const [addItemsToUnit] = useAddCatalogItemsToUnitMutation();

    const handleOk = async () => {
        if (selectedItems.length === 0 && selectedUnits.length === 0) {
            alert('Выберите хотябы один Item');
            return;
        }

        try {
            const postData: IAddUnitsAndItemsToKts = { 
                id: ktsId, items: selectedItems, units: selectedUnits 
            };
            // await addItemsToUnit(postData).unwrap();
            console.log(postData)
            setSelectedItems([]);
            setSelectedUnits([]);
            onCancel();
        } catch (error) {
            console.error('Ошибка при добавлении:', error);
        }
    };

    const toggleElement = (elementId: number, elementName: ITab) => {
        if (elementName === 'items') {
            setSelectedItems((prev) => {
                const exists = prev.find((el) => el.id === elementId);
                return exists
                    ? prev.filter((el) => el.id !== elementId)
                    : [...prev, { id: elementId, quantity: 1 }];
            });
        } else if (elementName === 'units') {
            setSelectedUnits((prev) => {
                const exists = prev.find((el) => el.id === elementId);
                return exists
                    ? prev.filter((el) => el.id !== elementId)
                    : [...prev, { id: elementId, quantity: 1 }];
            });
        }

    };

    const updateQuantity = (elementId: number, quantity: number, elementName: ITab) => {
        if (elementName === 'items') {
            if (quantity < 1) return;
            setSelectedItems((prev) =>
                prev.map((el) => (el.id === elementId ? { ...el, quantity } : el))
            );
        } else if (elementName === 'units') {
            if (quantity < 1) return;
            setSelectedUnits((prev) =>
                prev.map((el) => (el.id === elementId ? { ...el, quantity } : el))
            );
        }
    };

    const handleCancel = () => {
        setSelectedItems([]);
        setSelectedUnits([]);
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
            <Tabs
                activeKey={activeTab}
                onChange={(key) => setActiveTab(key as ITab)}
                items={[
                    { key: 'items', label: 'Units' },
                    { key: 'units', label: 'Items' },
                ]}
            />
            {isLoading || isError ? (
                <Loader isLoading={isLoading} isError={isError} />
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                    {activeTab === 'items' ? (
                        items?.map((item) => {
                            const isSelected = selectedItems.some((el) => el.id === item.id);
                            const quantity = selectedItems.find((el) => el.id === item.id)?.quantity || 1;

                            return (
                                <div
                                    key={item.id}
                                    onClick={() => toggleElement(item.id, 'items')}
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
                                                updateQuantity(item.id, Number(e.target.value), 'items')
                                            }
                                            onClick={(e) => e.stopPropagation()}
                                            style={{ width: 80, marginTop: 8 }}
                                            placeholder="Количество"
                                        />
                                    )}
                                </div>
                            );
                        })
                    ) : (
                        units?.map((unit) => {
                            const isSelected = selectedUnits.some((el) => el.id === unit.id);
                            const quantity = selectedUnits.find((el) => el.id === unit.id)?.quantity || 1;

                            return (
                                <div
                                    key={unit.id}
                                    onClick={() => toggleElement(unit.id, 'units')}
                                    style={{
                                        border: isSelected ? '2px solid #52c41a' : '',
                                        borderRadius: 8,
                                        padding: 6,
                                        cursor: 'pointer',
                                    }}
                                >
                                    <CatalogUnitCard unit={unit} />
                                    {isSelected && (
                                        <Input
                                            type="number"
                                            min={1}
                                            value={quantity}
                                            onChange={(e) =>
                                                updateQuantity(unit.id, Number(e.target.value), 'units')
                                            }
                                            onClick={(e) => e.stopPropagation()}
                                            style={{ width: 80, marginTop: 8 }}
                                            placeholder="Количество"
                                        />
                                    )}
                                </div>
                            );
                        })
                    )}
                </div>
            )}
        </Modal>
    );
};

export default AddUnitsAndItemsToKtsModal;
