/**
 * Created by haohao on 16-5-17.
 */
 KindEditor.ready(function(K) {
                K.create('textarea[name=content]',{
                    width:'800px',
                    height:'600px',
                    uploadJson: '/admin/upload/kindeditor',
                });
        });