import {
    Create,
    Form,
    Input,
    Select,
    useForm,
    useSelect,
} from "@pankod/refine-antd";

import { IBroker } from "interfaces";

export const BrokerCreate = () => {
    const { formProps, saveButtonProps } = useForm<IBroker>({
    });
    const { selectProps: brokerSelectProps } = useSelect<IBroker>({
        resource: "brokers",
        metaData:{
            fields: [
                "id",
                "name",
            ],
        },
        optionLabel: "name",
        optionValue: "id",
    });

    return (
        <Create saveButtonProps={saveButtonProps}>
            <Form {...formProps} layout="vertical">
                <Form.Item label="Name" name="name"
                           rules={[
                               {
                                   required: true,
                               },
                           ]}>
                    <Input />
                </Form.Item>
            </Form>
        </Create>
    );
};
