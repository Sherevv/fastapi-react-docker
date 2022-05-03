import {
    List,
    Table,
    useTable,
    getDefaultSortOrder, Space, EditButton, ShowButton, DeleteButton
} from "@pankod/refine-antd";

import { IBroker } from "interfaces";

export const BrokerList: React.FC = () => {
    const { tableProps, sorter } = useTable<IBroker>({
        initialCurrent: 1,
        initialPageSize: 10,
        metaData: {
            fields: [
                "id",
                "name",
            ],
        },
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
                <Table.Column<IBroker>
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