import React from 'react';
import { Modal, Form, Input } from 'antd';
import type { IProject } from '../../types/types';
import { useAddProjectMutation } from '../../redux/services/projectsApi';

interface AddProjectModalProps {
    isModalOpen: boolean;
    onCancel: () => void;
}

const AddProjectModal: React.FC<AddProjectModalProps> = ({ isModalOpen, onCancel }) => {

    const [form] = Form.useForm();
    const [addProject] = useAddProjectMutation();

    const handleOk = async () => {
        try {
            const values: IProject = await form.validateFields();
            await addProject({...values});
            form.resetFields();
            onCancel()
        } catch (error) {
            console.log('Validation Failed:', error);
        }
    };

    return (
        <Modal
            title="Добавить Проект"
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
                name="add_project_form"
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

export default AddProjectModal;
