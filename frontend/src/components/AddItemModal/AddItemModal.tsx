import React from 'react';
import { Modal, Form, Input } from 'antd';
import type { IItem } from '../../types/types';
import { useAddCatalogItemMutation } from '../../redux/services/catalogApi';

interface AddItemModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
}

const AddItemModal: React.FC<AddItemModalProps> = ({ isModalOpen, onCancel }) => {

    const [form] = Form.useForm();
    const [addItem] = useAddCatalogItemMutation();

    const handleOk = async () => {
        try {
            const values: IItem = await form.validateFields();
            await addItem({...values, currency: 'RUB'});
            form.resetFields();
            onCancel()
        } catch (error) {
            console.log('Validation Failed:', error);
        }
    };

    return (
        <Modal
            title="Добавить Item"
            open={isModalOpen}
            onCancel={() => {
                form.resetFields();
                onCancel();
            }}
            onOk={handleOk}
            okText="Сохранить"
            cancelText="Отмена"
        >
            <Form
                form={form}
                layout="vertical"
                name="add_item_form"
            >
                <Form.Item
                    name="name"
                    label="Название"
                    rules={[{ required: true, message: 'Введите название' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    name="description"
                    label="Описание"
                    rules={[{ required: true, message: 'Введите описание' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    name="supplier"
                    label="Поставщик"
                    rules={[{ required: true, message: 'Введите поставщик' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    name="catalog_code"
                    label="Код в каталоге"
                    rules={[{ required: true, message: 'Введите код в каталоге' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    name="price"
                    label="Цена"
                    rules={[
                        { required: true, message: 'Введите цену' },
                    ]}
                >
                    <Input />
                </Form.Item>

                <Form.Item 
                    name="manufactured" 
                    label="Производитель"
                    rules={[{ required: true, message: 'Введите производителя' }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item 
                    name="delivery_type" 
                    label="Tип доставки"
                    rules={[{ required: true, message: 'Введите тип доставки' }]}
                >
                    <Input />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default AddItemModal;
