import {CommonModule} from "@angular/common";
import {FormsModule} from "@angular/forms";
import {NgModule} from "@angular/core";
import {CoreEmailAdminComponent} from "./core-email-admin.component";
import {RouterModule, Routes} from "@angular/router";
import {SendTestTaskComponent} from "./send-test-task/send-test-task.component";
import {SendTestActivityComponent} from "./send-test-activity/send-test-activity.component";
import {
    TupleActionPushNameService,
    TupleActionPushService,
    TupleDataObservableNameService,
    TupleDataObserverService
} from "@synerty/vortexjs";

import {
    inboxActionProcessorName,
    inboxFilt,
    inboxObservableName
} from "@peek/peek_core_email/core-email-names";
import {AdminSettingListComponent} from "./setting-list/admin-setting-list.component";
import {AdminTaskListComponent} from "./task-list/admin-task-list.component";
import {AdminActivityListComponent} from "./activity-list/admin-activity-list.component";
/**
 * Created by peek on 5/12/16.
 *
 */


export const pluginRoutes: Routes = [
    {
        path: '',
        component: CoreEmailAdminComponent
    }

];


export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService(
        inboxObservableName, inboxFilt);
}

export function tupleActionPushNameServiceFactory() {
    return new TupleActionPushNameService(
        inboxActionProcessorName, inboxFilt);
}

@NgModule({
    imports: [
        CommonModule,
        FormsModule,
        RouterModule.forChild(pluginRoutes)],
    exports: [],
    providers: [
        TupleDataObserverService, {
            provide: TupleDataObservableNameService,
            useFactory: tupleDataObservableNameServiceFactory
        }, TupleActionPushService, {
            provide: TupleActionPushNameService,
            useFactory: tupleActionPushNameServiceFactory
        }
    ],
    declarations: [CoreEmailAdminComponent,
        AdminSettingListComponent,
    ]
})
export class CoreEmailAdminModule {

}