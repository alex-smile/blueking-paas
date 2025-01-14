<template lang="html">
    <div class="right-main">
        <div class="ps-top-bar">
            <h2> {{ $t('成员管理') }}
                <template v-if="pagination.count">
                    ({{pagination.count}}{{ $t('人') }})
                </template>
            </h2>
        </div>

        <paas-content-loader class="app-container middle" :is-loading="loading" placeholder="roles-loading">
            <div class="header mt10">
                <bk-button
                    theme="primary"
                    icon="plus"
                    v-if="enableToAddRole"
                    @click="createMember">
                    {{ $t('新增成员') }}
                </bk-button>
                <bk-input
                    class="search-input"
                    :placeholder="$t('请输入成员姓名，按Enter搜索')"
                    :clearable="true"
                    :right-icon="'bk-icon icon-search'"
                    v-model="keyword"
                    @enter="handleSearch">
                </bk-input>
            </div>
            <div class="content-wrapper">
                <bk-table
                    :data="memberListShow"
                    size="small"
                    :pagination="pagination"
                    @page-change="pageChange"
                    @page-limit-change="limitChange">
                    <bk-table-column :label="$t('成员姓名')">
                        <template slot-scope="props">
                            <span class="user-photo" v-if="props.row.user.avatar"><img :src="props.row.user.avatar" /></span>
                            <span class="user-name">{{props.row.user.username}}</span>
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="$t('角色')">
                        <template slot-scope="props">
                            <span class="role-name">{{ $t(roleNames[props.row.role.name]) }}</span>
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="$t('权限')" min-width="170">
                        <template slot-scope="props">
                            <span class="ps-pr" v-for="(perm, permIndex) in roleSpec[props.row.role.name]" :key="permIndex" v-if="perm[Object.keys(perm)[0]]">
                                {{ $t(Object.keys(perm)[0]) }}
                            </span>
                        </template>
                    </bk-table-column>
                    <bk-table-column :label="$t('操作')">
                        <template slot-scope="props">
                            <template v-if="canManageMe(props.row)">
                                <bk-button
                                    text
                                    class="mr5"
                                    @click="leaveApp(props.row.user.id, props.row.user.username)">
                                    {{ $t('退出应用') }}
                                </bk-button>
                            </template>
                            <bk-button
                                text
                                class="mr5"
                                v-if="canChangeMembers()"
                                @click="updateMember(props.row.user.id, props.row.user.username, props.row.role.name)">
                                {{ $t('更换角色') }}
                            </bk-button>
                            <bk-button
                                text
                                class="mr5"
                                v-if="canManageMembers(props.row)"
                                @click="delMember(props.row.user.username, props.row.user.id)">
                                {{ $t('删除成员') }}
                            </bk-button>
                        </template>
                    </bk-table-column>
                </bk-table>
            </div>
        </paas-content-loader>

        <bk-dialog
            width="540"
            v-model="memberMgrConfig.visiable"
            :title="memberMgrConfig.title"
            header-position="left"
            :theme="'primary'"
            :mask-close="false"
            :loading="memberMgrConfig.isLoading"
            @confirm="memberMgrSave"
            @cancel="closeMemberMgrModal"
            @after-leave="hookAfterClose">
            <div v-if="memberMgrConfig.showForm" style="min-height: 130px;">
                <bk-form :label-width="120" form-type="vertical">
                    <bk-form-item :label="$t('成员名称')" :required="true">
                        <template v-if="memberMgrConfig.userEditable">
                            <user v-model="personnelSelectorList"></user>
                            <!-- <bk-member-selector
                                @change="updateValue"
                                v-model="personnelSelectorList"
                                ref="member_selector">
                            </bk-member-selector> -->
                        </template>
                        <template v-else>
                            <bk-input :readonly="true" v-model="selectedMember.name"></bk-input>
                        </template>
                    </bk-form-item>
                    <bk-form-item :label="$t('角色')">
                        <bk-radio-group v-model="roleName">
                            <bk-radio :value="name" v-for="(chineseName, name) in roleNames" :key="name">{{$t(chineseName)}}</bk-radio>
                        </bk-radio-group>
                    </bk-form-item>
                    <bk-form-item :label="$t('权限列表')">
                        <div class="ps-rights-list">
                            <span v-for="(perm, permIndex) in roleSpec[roleName]" :key="permIndex">
                                <a class="available-right" v-if="perm[Object.keys(perm)[0]]">
                                    <span>{{ $t(Object.keys(perm)[0]) }}</span><i class="paasng-icon paasng-check-1"></i>
                                </a>
                                <a class="not-available-right" v-else>
                                    <span>{{ $t(Object.keys(perm)[0]) }}</span><i class="paasng-icon paasng-close"></i>
                                </a>
                            </span>
                        </div>
                    </bk-form-item>
                </bk-form>
            </div>
        </bk-dialog>

        <bk-dialog
            width="540"
            v-model="removeUserDialog.visiable"
            :title=" `${$t('删除成员 ')}${selectedMember.name}`"
            :theme="'primary'"
            :mask-close="false"
            :loading="removeUserDialog.isLoading"
            @confirm="delSave"
            @cancel="closeDelModal">
            <div class="tc">
                {{ $t('用户') }} {{ selectedMember.name }} {{ $t('将失去此应用的对应权限，是否确定删除？') }}
            </div>
        </bk-dialog>

        <bk-dialog
            width="540"
            v-model="leaveAppDialog.visiable"
            :title="$t('退出应用')"
            :theme="'primary'"
            :mask-close="false"
            :loading="leaveAppDialog.isLoading"
            @confirm="leaveSave"
            @cancel="closeLeaveApp">
            <div class="tc">
                {{ $t('退出并放弃此应用的对应权限，是否确定？') }}
            </div>
        </bk-dialog>

        <bk-dialog
            width="540"
            v-model="permissionNoticeDialog.visiable"
            :title="$t('权限须知')"
            :theme="'primary'"
            :mask-close="false"
            :loading="leaveAppDialog.isLoading">
            <div class="tc">
                {{ $t('由于应用目前使用了第三方源码托管系统，当管理员添加新的“开发者”角色用户后，需要同时在源码系统中添加对应的账号权限。否则无法进行正常开发工作') }}
            </div>
            <template slot="footer">
                <bk-button theme="primary" @click="iKnow"> {{ $t('我知道了') }} </bk-button>
            </template>
        </bk-dialog>
    </div>
</template>

<script>
    import { APP_ROLE_NAMES } from '@/common/constants';
    import auth from '@/auth';
    import appBaseMixin from '@/mixins/app-base-mixin';
    import user from '@/components/user';
    import i18n from '@/language/i18n.js';

    const ROLE_BACKEND_IDS = {
        'administrator': 2,
        'developer': 3,
        'operator': 4
    };

    const ROLE_SPEC = {
        'administrator': [
            {
                '应用开发': true
            },
            {
                '上线审核': true
            },
            {
                '应用推广': true
            },
            {
                '成员管理': true
            }
        ],
        'developer': [
            {
                '应用开发': true
            },
            {
                '上线审核': false
            },
            {
                '应用推广': true
            },
            {
                '成员管理': false
            }
        ],
        'operator': [
            {
                '应用开发': false
            },
            {
                '上线审核': true
            },
            {
                '应用推广': true
            },
            {
                '成员管理': false
            }
        ]
    };

    const ROLE_DESC_MAP = {
        'administrator': i18n.t('该角色仅影响用户在“开发者中心”管理该应用的权限，不涉及应用内部权限，请勿混淆')
    };

    export default {
        components: {
            user
        },
        mixins: [appBaseMixin],
        data () {
            return {
                currentUser: auth.getCurrentUser().username,
                hasPerm: false,
                loading: true,
                memberList: [],
                memberListShow: [],
                roleNames: APP_ROLE_NAMES,
                roleSpec: ROLE_SPEC,
                roleName: 'administrator',
                selectedMember: {
                    id: 0,
                    name: ''
                },
                personnelSelectorList: [],
                memberMgrConfig: {
                    visiable: false,
                    isLoading: false,
                    type: 'create',
                    userEditable: true,
                    title: this.$t('新增成员'),
                    showForm: false
                },
                leaveAppDialog: {
                    visiable: false,
                    isLoading: false
                },
                removeUserDialog: {
                    visiable: false,
                    isLoading: false
                },
                permissionNoticeDialog: {
                    visiable: false
                },

                pagination: {
                    current: 1,
                    count: 0,
                    limit: 10
                },
                currentBackup: 1,
                enableToAddRole: false,
                keyword: '',
                memberListClone: []
            };
        },
        computed: {
            currentRoleDesc () {
                return ROLE_DESC_MAP[this.roleName] || '';
            }
        },
        watch: {
            '$route' () {
                this.init();
            },
            'pagination.current' (value) {
                this.currentBackup = value;
            },
            keyword (val) {
                if (!val) {
                    this.handleSearch();
                }
            }
        },
        created () {
            this.init();
        },
        methods: {
            pageChange (page) {
                if (this.currentBackup === page) {
                    return;
                }
                this.pagination.current = page;

                this.handleSearch();
                // const start = this.pagination.limit * (this.pagination.current - 1)
                // const end = start + this.pagination.limit
                // this.memberListShow.splice(0, this.memberListShow.length, ...this.memberList.slice(start, end))
            },

            limitChange (currentLimit, prevLimit) {
                this.pagination.limit = currentLimit;
                this.pagination.current = 1;

                this.handleSearch();

                // const start = this.pagination.limit * (this.pagination.current - 1)
                // const end = start + this.pagination.limit
                // this.memberListShow.splice(0, this.memberListShow.length, ...this.memberList.slice(start, end))
            },

            iKnow () {
                this.permissionNoticeDialog.visiable = false;
                !localStorage.getItem('membersNoticeDialogHasShow') && localStorage.setItem('membersNoticeDialogHasShow', true);
            },

            updateValue (curVal) {
                curVal ? this.personnelSelectorList = curVal : this.personnelSelectorList = '';
            },

            init () {
                this.enableToAddRole = this.curAppInfo && this.curAppInfo.role.name === 'administrator';
                this.fetchMemberList();
                this.$nextTick(() => {
                    // 如果使用git
                    if (this.curAppDefaultModule.repo && this.curAppDefaultModule.repo.type.indexOf('git') > -1) {
                        if (!localStorage.getItem('membersNoticeDialogHasShow')) {
                            this.permissionNoticeDialog.visiable = true;
                        }
                    }
                });
            },

            async fetchMemberList () {
                try {
                    const res = await this.$store.dispatch('member/getMemberList', { appCode: this.appCode });

                    this.pagination.count = res.results.length;
                    const start = this.pagination.limit * (this.pagination.current - 1);
                    const end = start + this.pagination.limit;

                    this.hasPerm = true;

                    this.memberList.splice(0, this.memberList.length, ...(res.results || []));

                    this.memberListShow.splice(0, this.memberListShow.length, ...this.memberList.slice(start, end));
                } catch (e) {
                    this.hasPerm = false;
                    this.$paasMessage({
                        theme: 'error',
                        message: e.detail || this.$t('接口异常')
                    });
                } finally {
                    this.loading = false;
                }
            },

            createMember () {
                this.roleName = 'administrator';
                this.personnelSelectorList = [];
                this.memberMgrConfig = {
                    visiable: true,
                    isLoading: false,
                    type: 'create',
                    userEditable: true,
                    title: this.$t('新增成员'),
                    showForm: true
                };
            },

            hookAfterClose () {
                this.memberMgrConfig.showForm = false;
            },

            async createSave () {
                this.memberMgrConfig.isLoading = true;
                if (!this.personnelSelectorList.length) {
                    this.$paasMessage({
                        theme: 'error',
                        message: this.$t('请选择成员！')
                    });
                    setTimeout(() => {
                        this.memberMgrConfig.isLoading = false;
                    }, 100);
                    return;
                }

                let createParam = {};
                const createSuc = [];
                for (let i = 0; i < this.personnelSelectorList.length; i++) {
                    createParam = {
                        'application': {
                            'code': this.appCode
                        },
                        'user': {
                            'username': this.personnelSelectorList[i]
                        },
                        'role': {
                            'id': ROLE_BACKEND_IDS[this.roleName]
                        }
                    };
                    createSuc.push(createParam);
                }

                try {
                    await this.$store.dispatch('member/addMember', { appCode: this.appCode, postParams: createSuc });
                    this.closeMemberMgrModal();
                    this.fetchMemberList();
                    this.$paasMessage({
                        theme: 'success',
                        message: this.$t('新增成员成功！')
                    });
                } catch (e) {
                    this.$paasMessage({
                        theme: 'error',
                        message: `${this.$t('添加用户角色失败：')} ${e.detail}`
                    });
                } finally {
                    this.memberMgrConfig.isLoading = false;
                }
            },

            leaveApp (delMemberID, delMemberName) {
                this.selectedMember.id = delMemberID;
                this.selectedMember.name = delMemberName;
                this.leaveAppDialog.visiable = true;
            },

            async leaveSave () {
                try {
                    await this.$store.dispatch('member/quitApplication', { appCode: this.appCode });
                    this.closeLeaveApp();
                    this.$router.push({
                        path: '/'
                    });
                } catch (e) {
                    this.closeLeaveApp();
                    this.$paasMessage({
                        theme: 'error',
                        message: `${this.$t('退出应用失败：')} ${e.detail}`
                    });
                } finally {
                    this.leaveAppDialog.isLoading = false;
                }
            },

            closeLeaveApp () {
                this.leaveAppDialog.visiable = false;
            },

            updateMember (updateMemberID, updateMemberName, updateMemberRole) {
                this.selectedMember.id = updateMemberID;
                this.selectedMember.name = updateMemberName;
                this.roleName = updateMemberRole;
                this.memberMgrConfig = {
                    visiable: true,
                    isLoading: false,
                    type: 'edit',
                    userEditable: false,
                    title: this.$t('更换角色'),
                    showForm: true
                };
            },

            memberMgrSave () {
                const mgrType = this.memberMgrConfig.type;
                if (mgrType === 'edit') {
                    return this.updateSave();
                } else if (mgrType === 'create') {
                    return this.createSave();
                }
            },

            async updateSave () {
                const updateParam = {
                    'role': {
                        'id': ROLE_BACKEND_IDS[this.roleName]
                    }
                };
                this.memberMgrConfig.isLoading = true;
                try {
                    await this.$store.dispatch('member/updateRole', { appCode: this.appCode, id: this.selectedMember.id, params: updateParam });
                    this.closeMemberMgrModal();
                    this.fetchMemberList();
                    this.$paasMessage({
                        theme: 'success',
                        message: this.$t('角色更新成功！')
                    });
                    if (this.selectedMember.name === this.currentUser && this.roleName !== 'administrator') {
                        this.enableToAddRole = false;
                    }
                } catch (e) {
                    this.$paasMessage({
                        theme: 'error',
                        message: `${this.$t('修改角色失败：')} ${e.detail}`
                    });
                } finally {
                    this.memberMgrConfig.isLoading = false;
                }
            },

            delMember (delMemberName, delMemberID) {
                this.selectedMember.id = delMemberID;
                this.selectedMember.name = delMemberName;
                this.removeUserDialog.visiable = true;
            },

            async delSave () {
                try {
                    await this.$store.dispatch('member/deleteRole', { appCode: this.appCode, id: this.selectedMember.id });
                    this.closeDelModal();
                    this.$paasMessage({
                        theme: 'success',
                        message: this.$t('删除成员成功！')
                    });
                    this.fetchMemberList();
                } catch (e) {
                    this.$paasMessage({
                        theme: 'error',
                        message: `${this.$t('删除成员失败：')} ${e.detail}`
                    });
                }
            },

            closeDelModal () {
                this.removeUserDialog.visiable = false;
            },

            closeMemberMgrModal () {
                this.memberMgrConfig.visiable = false;
            },

            canManageMe (roleInfo) {
                if (roleInfo.user.username !== this.currentUser) {
                    return false;
                }
                if (roleInfo.user.id === this.curAppInfo.application.owner) {
                    return false;
                }
                return true;
            },

            canManageMembers (roleInfo) {
                if (roleInfo.user.username === this.currentUser || !this.enableToAddRole) {
                    // 不能操作自身角色 || 非管理员不能操作角色管理
                    return false;
                }
                return true;
            },

            canChangeMembers () {
                if (!this.enableToAddRole) {
                    return false;
                }
                return true;
            },
            handleSearch () {
                if (this.keyword) {
                    this.memberListShow = this.memberList.filter(apigw => {
                        return apigw.user.username.toLowerCase().indexOf(this.keyword.toLowerCase()) > -1;
                    });
                    this.memberListClone = [...this.memberListShow];
                    this.pagination.count = this.memberListClone.length;
                    if (this.memberListClone.length > 10) {
                        const start = this.pagination.limit * (this.pagination.current - 1);
                        const end = start + this.pagination.limit;
                        this.memberListShow.splice(0, this.memberListShow.length, ...this.memberListClone.slice(start, end));
                    }
                } else {
                    this.fetchMemberList();
                }
            }
        }
    };
</script>

<style lang="scss" scoped>
    .content-wrapper {
        margin-top: 16px;
    }
    .search-input {
         width: 360px;
         display: inline-block;
    }
    .user-photo {
        margin: 5px 0;
        display: inline-block;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        overflow: hidden;
        border: solid 1px #eaeaea;
        vertical-align: middle;

        img {
            width: 100%;
            height: 100%;
        }
    }

    .user-name {
        display: inline-block;
        padding-left: 10px;
        font-size: 14px;
        color: #333;
        vertical-align: middle;
    }

    .ps-pr {
        padding-right: 15px;
        color: #999;
    }

    .middle {
        padding-top: 15px;
    }

    .ps-rights-list {
        line-height: 36px;

        a {
            margin-right: 7px;
            padding: 6px 15px;
            font-size: 13px;
            line-height: 1;
            border-radius: 14px;
            color: #666;
            cursor: default;

            &.available-right {
                border: 1px solid #3A84FF;

                i {
                    color: #3A84FF;
                    transform: scale(.95);
                }
            }

            &.not-available-right {
                border: 1px solid #ddd;
                color: #ddd;

                i {
                    transform: scale(.75);
                }
            }

            i {
                display: inline-block;
                margin-left: 3px;
            }
        }
    }
</style>
