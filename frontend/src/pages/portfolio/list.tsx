import {
    List,
    Table,
    useTable,
    useSelect, getDefaultSortOrder, FilterDropdown, Space, EditButton, ShowButton, DeleteButton, Select
} from "@pankod/refine-antd";

import { IBroker, IPortfolio } from "interfaces";

export const PortfolioList: React.FC = () => {
    const { tableProps, sorter } = useTable<IPortfolio>({
        resource: "portfolios",
        initialSorter: [
            {
                field: "id",
                order: "desc",
            },
        ],
        initialCurrent: 1,
        initialPageSize: 10,
        initialFilter: [
            {
                operator: "or",
                value: [
                    // {
                    //     field: "name",
                    //     operator: "contains",
                    //     value: "s",
                    // },
                    // {
                    //     field: "name",
                    //     operator: "ncontains",
                    //     value: "d",
                    // },
                    // {
                    //     field: "name",
                    //     operator: "containss",
                    //     value: "s",
                    // },
                    // {
                    //     field: "name",
                    //     operator: "ncontainss",
                    //     value: "d",
                    // },
                    // {
                    //     field: "id",
                    //     operator: "gt",
                    //     value: 2,
                    // },
                    // {
                    //     field: "id",
                    //     operator: "gte",
                    //     value: 2,
                    // },
                    // {
                    //     field: "id",
                    //     operator: "lt",
                    //     value: 5,
                    // },
                    // {
                    //     field: "id",
                    //     operator: "lte",
                    //     value: 5,
                    // },
                    // {
                    //     field: "id",
                    //     operator: "between",
                    //     value: [1,3],
                    // },
                    // {
                    //     field: "id",
                    //     operator: "nbetween",
                    //     value: [4,6],
                    // },
                    // {
                    //     field: "id",
                    //     operator: "null",
                    //     value: null,
                    // },
                    // {
                    //     field: "id",
                    //     operator: "nnull",
                    //     value: null,
                    // },
                ],

            },
            // {
            //     field: "name",
            //     operator: "eq",
            //     value: "s",
            // }
        ],
        metaData: {
            fields: [
                "id",
                "name",
                {
                    broker: [
                        //"id",
                        "name"
                    ],
                },
            ],
            // variables:
            //     {
            //         name:"string"
            //     }
        },
    });

    const { selectProps: brokerSelectProps } = useSelect<IBroker>({
        resource: "brokers",
        metaData: {
            fields: ["id", "name"],
        },
        optionLabel: "name",
        optionValue: "id",
        // onSearch: (value) => [
        //     {
        //         field: "id",
        //         operator: "eq",
        //         value,
        //     },
        // ],
    });

    return (
        <List>
            <Table {...tableProps} rowKey="id">
                <Table.Column
                    dataIndex="id"
                    title="ID"
                    sorter={{ multiple: 2 }}
                    defaultSortOrder={getDefaultSortOrder("id", sorter)}
                />
                <Table.Column dataIndex="name" title="Name" />
                <Table.Column<IPortfolio>
                    dataIndex="broker_id"
                    title="Broker"

                    filterDropdown={(props) => (
                        <FilterDropdown {...props}
                                        mapValue={(selectedKeys) =>
                                            selectedKeys.map((i) => parseInt(i.toString()))
                                        }>
                            <Select
                                style={{ minWidth: 200 }}
                                mode="multiple"
                                placeholder="Select Broker"
                                {...brokerSelectProps}
                            />
                        </FilterDropdown>
                    )}
                    render={(_, record) => {
                        return record.broker ? record.broker.name : ''
                    }}
                />
                <Table.Column<IPortfolio>
                    title="Actions"
                    dataIndex="actions"
                    render={(_, record) => (
                        <Space>
                            <EditButton
                                hideText
                                size="small"
                                recordItemId={record.id}
                            />
                            <ShowButton
                                hideText
                                size="small"
                                recordItemId={record.id}
                            />
                            <DeleteButton
                                hideText
                                size="small"
                                recordItemId={record.id}
                            />
                        </Space>
                    )}
                />
            </Table>
        </List>
    );
};