import React from 'react';
import { Modal, Form, Input } from 'antd';
import type { IItem } from '../../types/types';
import { useAddCatalogUnitMutation } from '../../redux/services/catalogApi';

interface AddUnitModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
}

const AddUnitModal: React.FC<AddUnitModalProps> = ({ isModalOpen, onCancel }) => {

    const [form] = Form.useForm();
    const [addUnit] = useAddCatalogUnitMutation();

    const handleOk = async () => {
        try {
            const values: IItem = await form.validateFields();
            await addUnit({...values});
            form.resetFields();
            onCancel()
        } catch (error) {
            console.log('Validation Failed:', error);
        }
    };

    return (
        <Modal
            title="Добавить Unit"
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
                name="add_unit_form"
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
            </Form>
        </Modal>
    );
};

export default AddUnitModal;
