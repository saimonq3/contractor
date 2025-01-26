pipeline {
    agent {
        any {
            label 'dev'
        }
    }
    parameters {
        listGitBranches branchFilter: 'refs/heads/(.*)',
        defaultValue: 'dev',
        name: 'BRANCH_FROM',
        type: 'PT_BRANCH',
        remoteURL: 'https://git.tolq3.ru/manhattan/contractor.git',
        credentialsId: '576718b4-fe42-4810-99fb-205be3ae9b9f',
        selectedValue: 'DEFAULT',
        sortMode: 'ASCENDING'
        // gitParameter(name: 'BRANCH_TAG', type: 'PT_BRANCH_TAG', branchFilter: 'origin/(.*)', defaultValue: 'dev', selectedValue: 'DEFAULT', sortMode: 'DESCENDING_SMART', description: 'Выбирете ветку которую хотите слить')
		// choice(name: 'SonarQube', choices: ['False','True'],description: '')
        // string('name': 'BRANCH_TAG', defaultValue: 'dev')
         listGitBranches branchFilter: 'refs/heads/(.*)',
        defaultValue: 'dev',
        name: 'BRANCH_TO',
        type: 'PT_BRANCH',
        remoteURL: 'https://git.tolq3.ru/manhattan/contractor.git',
        credentialsId: '576718b4-fe42-4810-99fb-205be3ae9b9f',
        selectedValue: 'DEFAULT',
        sortMode: 'ASCENDING'
    }
    stages {
        stage('clone repo') {
            steps{
                checkout([$class                           : 'GitSCM', branches: [[name: "${params.BRANCH_TO}"]],
                          doGenerateSubmoduleConfigurations: false,
                          extensions                       : [],
                          submoduleCfg                     : [],
                          gitTool: 'Default',
                          userRemoteConfigs                : [[credentialsId: '576718b4-fe42-4810-99fb-205be3ae9b9f',
                                                               url          :  'https://git.tolq3.ru/manhattan/contractor.git']]
                          ])
            }
        }
        stage('run tests') {
            steps{
                echo 'tests'
            }
        }
        stage('run build') {
            steps{
                echo 'build'
            }
        }
    }
}
