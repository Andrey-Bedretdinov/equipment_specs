import React from 'react';
import { Modal, Form, Input } from 'antd';
import type { IItem } from '../../types/types';
import { useAddCatalogKtsMutation } from '../../redux/services/catalogApi';

interface AddKtsModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
}

const AddKtsModal: React.FC<AddKtsModalProps> = ({ isModalOpen, onCancel }) => {

    const [form] = Form.useForm();
    const [addKts] = useAddCatalogKtsMutation();

    const handleOk = async () => {
        try {
            const values: IItem = await form.validateFields();
            await addKts({...values});
            form.resetFields();
            onCancel()
        } catch (error) {
            console.log('Validation Failed:', error);
        }
    };

    return (
        <Modal
            title="Добавить Kts"
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
                name="add_kts_form"
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

export default AddKtsModal;
