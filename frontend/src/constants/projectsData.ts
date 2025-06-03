import type { ProjectNode } from '../types/types';

export const projectsData: ProjectNode[] = [
    {
        id: 1,
        name: 'Проект модернизации линии',
        description: 'Модернизация электрической и осветительной части линии.',
        kts: [
            {
                id: 11,
                name: 'КТС-Электроснабжение',
                description: 'Комплект технических средств для электроснабжения.',
                quantity: 1,
                untis: [
                    {
                        id: 111,
                        name: 'Щит управления',
                        description: 'Щит управления для производственной линии.',
                        quantity: 1,
                        items: [
                            {
                                id: 1111,
                                name: 'Контактор ABB',
                                description: 'Контактор на 100А для автоматизации цепей.',
                                supplier: 'ООО "ЭлектроСнаб"',
                                catalog_code: 'ABB-CT100',
                                price: 1500,
                                currency: 'RUB',
                                manufacturer: 'ABB',
                                deliveryType: 'Склад',
                                quantity: 10,
                            },
                            {
                                id: 1112,
                                name: 'Автомат Schneider',
                                description: 'Автоматический выключатель на 60А.',
                                supplier: 'ЗАО "ТехноПоставка"',
                                catalog_code: 'SCH-B60',
                                price: 1200,
                                currency: 'RUB',
                                manufacturer: 'Schneider Electric',
                                deliveryType: 'Под заказ',
                                quantity: 5,
                            },
                        ],
                    },
                    {
                        id: 112,
                        name: 'Панель освещения',
                        description: 'Осветительная панель для цеха.',
                        quantity: 1,
                        items: [
                            {
                                id: 1121,
                                name: 'Светильник LED',
                                description: 'Потолочный светильник 45Вт.',
                                supplier: 'ИП Иванов',
                                catalog_code: 'LED-L45',
                                price: 800,
                                currency: 'RUB',
                                manufacturer: 'GALAD',
                                deliveryType: 'Склад',
                                quantity: 20,
                            },
                        ],
                    },
                ],
            },
        ],
    },
    {
        id: 2,
        name: 'Проект автоматизации склада',
        description: 'Автоматизация процессов управления складом.',
        kts: [
            {
                id: 21,
                name: 'КТС-СКУД',
                description: 'Система контроля и управления доступом.',
                quantity: 1,
                untis: [
                    {
                        id: 211,
                        name: 'Серверная стойка',
                        description: 'Оборудование для хранения и обработки данных.',
                        quantity: 1,
                        items: [
                            {
                                id: 2111,
                                name: 'Сервер HP ProLiant',
                                description: 'Сервер для установки системы контроля.',
                                supplier: 'ООО "СерверМаркет"',
                                catalog_code: 'HP-DL360',
                                price: 85000,
                                currency: 'RUB',
                                manufacturer: 'HP',
                                deliveryType: 'Под заказ',
                                quantity: 2,
                            },
                        ],
                    },
                    {
                        id: 212,
                        name: 'Считыватели карт',
                        description: 'RFID считыватели для доступа на склад.',
                        quantity: 3,
                        items: [
                            {
                                id: 2121,
                                name: 'Считыватель ZKTeco',
                                description: 'Бесконтактный RFID-считыватель.',
                                supplier: 'ЗАО "Безопасность+"',
                                catalog_code: 'ZK-RFID200',
                                price: 4500,
                                currency: 'RUB',
                                manufacturer: 'ZKTeco',
                                deliveryType: 'Склад',
                                quantity: 6,
                            },
                        ],
                    },
                ],
            },
        ],
    },
];
