import React, { useState } from 'react';
import { Modal, Input, Tabs } from 'antd';
import type { IAddOrDeleteElementsToProjects } from '../../types/types';
import {
    useGetCatalogItemsQuery,
    useGetCatalogUnitsQuery,
    useGetCatalogKtsQuery,
} from '../../redux/services/catalogApi';
import CatalogItemCard from '../CatalogItemCard/CatalogItemCard';
import CatalogUnitCard from '../CatalogUnitCard/CatalogUnitCard';
import CatalogKtsCard from '../CatalogKtsCard/CatalogKtsCard';
import Loader from '../Loader/Loader';
import { useAddElementsToProjectMutation } from '../../redux/services/projectsApi';

interface AddElementsModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
    projectId: number;
}

type ITab = 'items' | 'units' | 'kts';

const AddElementsToProjectModal: React.FC<AddElementsModalProps> = ({
    isModalOpen,
    onCancel,
    projectId
}) => {
    const [selectedItems, setSelectedItems] = useState<{ item_id: number; quantity: number }[]>([]);
    const [selectedUnits, setSelectedUnits] = useState<{ unit_id: number; quantity: number }[]>([]);
    const [selectedKts, setSelectedKts] = useState<{ kts_id: number; quantity: number }[]>([]);
    const [activeTab, setActiveTab] = useState<ITab>('items');

    const { data: items, isError: isItemsError, isLoading: isItemsLoading } = useGetCatalogItemsQuery();
    const { data: units, isError: isUnitsError, isLoading: isUnitsLoading } = useGetCatalogUnitsQuery();
    const { data: kts, isError: isKtsError, isLoading: isKtsLoading } = useGetCatalogKtsQuery();
    const [addElementsToProject] = useAddElementsToProjectMutation();

    const handleOk = async () => {
        if (selectedItems.length === 0 && selectedUnits.length === 0 && selectedKts.length === 0) {
            alert('Выберите хотя бы один Item, Unit или KTS');
            return;
        }

        try {
            const postData: IAddOrDeleteElementsToProjects = {
                items: selectedItems,
                units: selectedUnits,
                kts: selectedKts,
            };
            addElementsToProject({id: projectId, ...postData})
            setSelectedItems([]);
            setSelectedUnits([]);
            setSelectedKts([]);
            onCancel();
        } catch (error) {
            console.error('Ошибка при добавлении:', error);
        }
    };

    const toggleSelection = (id: number, type: ITab) => {
        switch (type) {
            case 'items':
                setSelectedItems(prev =>
                    prev.some(el => el.item_id === id)
                        ? prev.filter(el => el.item_id !== id)
                        : [...prev, { item_id: id, quantity: 1 }]
                );
                break;
            case 'units':
                setSelectedUnits(prev =>
                    prev.some(el => el.unit_id === id)
                        ? prev.filter(el => el.unit_id !== id)
                        : [...prev, { unit_id: id, quantity: 1 }]
                );
                break;
            case 'kts':
                setSelectedKts(prev =>
                    prev.some(el => el.kts_id === id)
                        ? prev.filter(el => el.kts_id !== id)
                        : [...prev, { kts_id: id, quantity: 1 }]
                );
                break;
        }
    };

    const changeQuantity = (id: number, quantity: number, type: ITab) => {
        if (quantity < 1) return;
        switch (type) {
            case 'items':
                setSelectedItems(prev =>
                    prev.map(el => (el.item_id === id ? { ...el, quantity } : el))
                );
                break;
            case 'units':
                setSelectedUnits(prev =>
                    prev.map(el => (el.unit_id === id ? { ...el, quantity } : el))
                );
                break;
            case 'kts':
                setSelectedKts(prev =>
                    prev.map(el => (el.kts_id === id ? { ...el, quantity } : el))
                );
                break;
        }
    };

    const renderSelectableList = <T extends { id: number }>(
        data: T[] | undefined,
        selectedList: { item_id?: number; unit_id?: number; kts_id?: number; quantity: number }[],
        type: ITab,
        renderCard: (item: T) => React.ReactNode,
        selectedColor: string
    ) => {
        return data?.map((item) => {
            const itemIdKey = type === 'items' ? 'item_id' : type === 'units' ? 'unit_id' : 'kts_id';
            const isSelected = selectedList.some((el) => el[itemIdKey] === item.id);
            const quantity = selectedList.find((el) => el[itemIdKey] === item.id)?.quantity || 1;

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
